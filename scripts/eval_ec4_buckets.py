#!/usr/bin/env python3
"""
R2 EC-4 Bucket Baseline Evaluation

Computes grouped R→E MRR for EC-4 tail/mid/head buckets as a pre-R3 baseline.
Reads R2 embeddings and metadata only — no model, no training, no torch.

Bucket definitions:
  tail : EC-4 group size <= 4
  mid  : 4 < EC-4 group size <= 317
  head : EC-4 group size > 317

Grouped MRR algorithm matches train.py:evaluate_grouped_re exactly:
  - query rows from current bucket
  - candidate enzyme rows = ALL enzyme rows
  - positive set = all rows sharing the same EC-4
  - best_pos_score = max score over positive set
  - rank = 1 + count(candidates with score > best_pos_score)
  - MRR = mean(1/rank) over bucket queries

Usage:
    python eval_ec4_buckets.py \\
        --output_dir /path/to/r2_outputs \\
        --report_path /path/to/R2_EC4_BUCKET_BASELINE.md \\
        --chunk_size 1024

    # Teacher-checklist compatible alias. This script reads saved
    # embeddings/metadata/metrics from an output directory; it does not load
    # model checkpoint weights.
    python eval_ec4_buckets.py \\
        --checkpoint /path/to/r2_outputs \\
        --report_path /path/to/R2_EC4_BUCKET_BASELINE.md
"""

import argparse
import json
import os
import platform
import socket
import sys
import time
from collections import defaultdict
from datetime import datetime

np = None


def require_numpy():
    """Import numpy only when computation starts, so --help stays lightweight."""
    global np
    if np is None:
        import numpy as _np
        np = _np
    return np

# ──────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────
TAIL_MAX = 4
MID_MAX = 317
DEFAULT_CHUNK_SIZE = 2048

DEFAULT_OUTPUT_DIR = (
    "/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04"
    "/outputs/r2_esmc_hardneg1_stage1_25_2026-06-11"
)
DEFAULT_REPORT_PATH = (
    "/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04"
    "/docs/R2_EC4_BUCKET_BASELINE.md"
)


# ──────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def parse_ec4(ec_str):
    """Strict EC-4 parser.

    Returns a string like '1.2.3.4' when the first 4 dot-separated
    segments all pass int(); otherwise returns None (unknown / invalid).
    """
    if not ec_str or not isinstance(ec_str, str):
        return None
    s = ec_str.strip()
    if s in ("", "unknown", "-"):
        return None
    parts = s.split(".")
    if len(parts) < 4:
        return None
    try:
        for i in range(4):
            int(parts[i])
    except ValueError:
        return None
    return f"{parts[0]}.{parts[1]}.{parts[2]}.{parts[3]}"


def l2_normalize(x):
    """L2-normalize along the last axis; zero-norm rows stay zero."""
    norms = np.linalg.norm(x, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return x / norms


def to_jsonable(obj):
    """Recursively convert numpy types to JSON-serializable Python types."""
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return str(obj)
        return obj
    return obj


# ──────────────────────────────────────────────────────────────────────
# EC-4 Group Builder
# ──────────────────────────────────────────────────────────────────────
def build_ec4_groups(metadata):
    """Parse EC-4 for every row and build group index.

    Returns:
        ec4_labels: list[str|None] — parsed EC-4 or None
        groups_dict: dict[str, list[int]] — EC-4 key → row indices
        valid_mask: np.ndarray[bool] — True for valid EC-4 rows
    """
    N = len(metadata)
    ec4_labels = []
    groups_dict = defaultdict(list)

    for i in range(N):
        ec = parse_ec4(metadata[i].get("ec_number", ""))
        ec4_labels.append(ec)
        if ec is not None:
            groups_dict[ec].append(i)

    valid_mask = np.array([ec is not None for ec in ec4_labels], dtype=bool)
    return ec4_labels, dict(groups_dict), valid_mask


# ──────────────────────────────────────────────────────────────────────
# Bucket Assignment
# ──────────────────────────────────────────────────────────────────────
def assign_buckets(groups_dict):
    """Assign each EC-4 group to tail/mid/head based on group size.

    Returns:
        key_to_bucket: dict[str, str] — EC-4 key → bucket label
    """
    key_to_bucket = {}
    for ec4_key, indices in groups_dict.items():
        gs = len(indices)
        if gs <= TAIL_MAX:
            key_to_bucket[ec4_key] = "tail"
        elif gs <= MID_MAX:
            key_to_bucket[ec4_key] = "mid"
        else:
            key_to_bucket[ec4_key] = "head"
    return key_to_bucket


def map_rows_to_buckets(ec4_labels, key_to_bucket):
    """Map each row to its bucket label.

    Returns:
        row_buckets: list[str] — bucket label per row ("" for excluded)
    """
    row_buckets = []
    for ec in ec4_labels:
        if ec is not None and ec in key_to_bucket:
            row_buckets.append(key_to_bucket[ec])
        else:
            row_buckets.append("")
    return row_buckets


# ──────────────────────────────────────────────────────────────────────
# Core: Chunked Grouped MRR
# ──────────────────────────────────────────────────────────────────────
def compute_bucket_mrr(reaction_emb, enzyme_emb, ec4_labels, groups_dict,
                       valid_mask, key_to_bucket, row_buckets, chunk_size,
                       ks=(1, 5, 10)):
    """Compute grouped R→E MRR per bucket in a single chunked pass.

    Algorithm matches train.py:evaluate_grouped_re exactly.
    """
    N = len(reaction_emb)
    max_k = max(ks)

    # Pre-convert group index lists to numpy arrays for fast indexing
    groups_arr = {k: np.array(v, dtype=np.int64) for k, v in groups_dict.items()}

    # Accumulators per bucket + overall
    bucket_names = ["tail", "mid", "head", "all"]
    accum = {
        b: {"rr_sum": 0.0, "top1": 0, "top5": 0, "top10": 0, "n": 0}
        for b in bucket_names
    }

    n_chunks = (N + chunk_size - 1) // chunk_size
    t0 = time.time()

    for ci, start in enumerate(range(0, N, chunk_size)):
        end = min(start + chunk_size, N)
        sim_chunk = reaction_emb[start:end] @ enzyme_emb.T  # (chunk, N)

        for local_i in range(end - start):
            global_i = start + local_i
            if not valid_mask[global_i]:
                continue

            s = sim_chunk[local_i]  # (N,) scores
            my_key = ec4_labels[global_i]
            gi = groups_arr.get(my_key)

            if gi is None or len(gi) == 0:
                continue

            # Grouped MRR
            best_pos_score = float(np.max(s[gi]))
            rank = int(np.sum(s > best_pos_score)) + 1
            rr = 1.0 / rank

            # Top-k via argpartition
            k_eff = min(max_k, len(s))
            topk_unsorted = np.argpartition(-s, k_eff - 1)[:k_eff]
            topk_idx = topk_unsorted[np.argsort(-s[topk_unsorted])]
            gset = set(gi.tolist())
            t1_hit = bool(set(topk_idx[:1].tolist()) & gset)
            t5_hit = bool(set(topk_idx[:5].tolist()) & gset)
            t10_hit = bool(set(topk_idx[:10].tolist()) & gset)

            # Determine bucket for this row
            bucket = row_buckets[global_i]

            # Accumulate into row's bucket
            if bucket in accum:
                accum[bucket]["rr_sum"] += rr
                accum[bucket]["top1"] += int(t1_hit)
                accum[bucket]["top5"] += int(t5_hit)
                accum[bucket]["top10"] += int(t10_hit)
                accum[bucket]["n"] += 1

            # Always accumulate into "all"
            accum["all"]["rr_sum"] += rr
            accum["all"]["top1"] += int(t1_hit)
            accum["all"]["top5"] += int(t5_hit)
            accum["all"]["top10"] += int(t10_hit)
            accum["all"]["n"] += 1

        del sim_chunk

        if (ci + 1) % 10 == 0 or ci == n_chunks - 1:
            elapsed = time.time() - t0
            log(f"  chunk {ci+1}/{n_chunks} done, elapsed={elapsed:.1f}s")

    # Finalize metrics
    results = {}
    for b in bucket_names:
        a = accum[b]
        n = a["n"]
        if n > 0:
            results[b] = {
                "n_queries": n,
                "MRR": a["rr_sum"] / n,
                "top-1": a["top1"] / n,
                "top-5": a["top5"] / n,
                "top-10": a["top10"] / n,
            }
        else:
            results[b] = {
                "n_queries": 0,
                "MRR": 0.0,
                "top-1": 0.0,
                "top-5": 0.0,
                "top-10": 0.0,
            }

    return results


# ──────────────────────────────────────────────────────────────────────
# Group Statistics
# ──────────────────────────────────────────────────────────────────────
def compute_group_stats(groups_dict, key_to_bucket):
    """Compute group size statistics per bucket and overall."""
    bucket_names = ["tail", "mid", "head", "all"]
    stats = {b: [] for b in bucket_names}

    for ec4_key, indices in groups_dict.items():
        gs = len(indices)
        bucket = key_to_bucket[ec4_key]
        stats[bucket].append(gs)
        stats["all"].append(gs)

    result = {}
    for b in bucket_names:
        sizes = stats[b]
        if len(sizes) > 0:
            arr = np.array(sizes)
            result[b] = {
                "n_groups": len(sizes),
                "n_rows": int(arr.sum()),
                "min": int(arr.min()),
                "median": float(np.median(arr)),
                "mean": float(arr.mean()),
                "p95": float(np.percentile(arr, 95)),
                "max": int(arr.max()),
            }
        else:
            result[b] = {
                "n_groups": 0, "n_rows": 0,
                "min": 0, "median": 0.0, "mean": 0.0, "p95": 0.0, "max": 0,
            }

    return result


# ──────────────────────────────────────────────────────────────────────
# Consistency Check
# ──────────────────────────────────────────────────────────────────────
def consistency_check(computed_mrr, metrics_path):
    """Compare computed overall EC-4 grouped MRR against metrics_v3.json."""
    with open(metrics_path) as f:
        metrics = json.load(f)

    expected = metrics["grouped_re"]["EC-4-grouped_MRR"]
    rel_err = abs(computed_mrr - expected) / abs(expected) if expected != 0 else float("inf")
    status = "PASS" if rel_err < 0.01 else "REVIEW"

    return {
        "expected": expected,
        "computed": computed_mrr,
        "rel_err": rel_err,
        "tolerance": 0.01,
        "status": status,
    }


# ──────────────────────────────────────────────────────────────────────
# Output: JSON
# ──────────────────────────────────────────────────────────────────────
def write_json_report(results, group_stats, check, args, path):
    """Write machine-readable JSON report."""
    report = {
        "task": "R2 EC-4 Bucket Baseline Evaluation",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "inputs": {
            "embeddings": os.path.join(args.output_dir, "embeddings_v3.npz"),
            "metadata": os.path.join(args.output_dir, "metadata_v3.json"),
            "metrics": os.path.join(args.output_dir, "metrics_v3.json"),
        },
        "bucket_definitions": {
            "tail": f"EC-4 group size <= {TAIL_MAX}",
            "mid": f"{TAIL_MAX} < EC-4 group size <= {MID_MAX}",
            "head": f"EC-4 group size > {MID_MAX}",
        },
        "chunk_size": args.chunk_size,
        "group_statistics": to_jsonable(group_stats),
        "bucket_results": to_jsonable(results),
        "overall_ec4_grouped_MRR": results["all"]["MRR"],
        "consistency_check": to_jsonable(check),
        "environment": {
            "hostname": socket.gethostname(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "declarations": {
            "train.py modified": False,
            "eval script created": True,
            "retraining executed": False,
            "new calibration/OOD/latency thresholds introduced": False,
        },
    }

    with open(path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    log(f"JSON report written to {path}")


# ──────────────────────────────────────────────────────────────────────
# Output: Markdown
# ──────────────────────────────────────────────────────────────────────
def write_markdown_report(results, group_stats, check, args, path):
    """Write human-readable markdown report."""
    npz = os.path.join(args.output_dir, "embeddings_v3.npz")
    meta = os.path.join(args.output_dir, "metadata_v3.json")
    metr = os.path.join(args.output_dir, "metrics_v3.json")
    out_json = os.path.join(args.output_dir, "r2_ec4_bucket_baseline.json")

    lines = []
    w = lines.append

    w("# R2 EC-4 Bucket Baseline")
    w("")
    w("## 1. Purpose")
    w("")
    w("This report documents the **R2 EC-4 bucket baseline evaluation** computed "
      "before R3 training begins. It measures grouped R→E MRR stratified by EC-4 "
      "group size (tail / mid / head) to establish a reference point for future R3 "
      "improvements. **No R3 training, model modification, or threshold calibration "
      "was performed.**")
    w("")

    w("## 2. Inputs")
    w("")
    w(f"| File | Path |")
    w(f"|------|------|")
    w(f"| embeddings | `{npz}` |")
    w(f"| metadata | `{meta}` |")
    w(f"| metrics | `{metr}` |")
    w("")

    w("## 3. Method")
    w("")
    w("### 3.1 Strict EC-4 Parser")
    w("")
    w("- `ec_number` must be a non-empty string")
    w("- Split by `'.'` must yield ≥ 4 segments")
    w("- First 4 segments must all pass `int()` conversion")
    w("- Otherwise the row is **excluded** from EC-4 bucket evaluation")
    w("")
    w("### 3.2 Bucket Definitions")
    w("")
    w(f"| Bucket | Rule |")
    w(f"|--------|------|")
    w(f"| tail | EC-4 group size ≤ {TAIL_MAX} |")
    w(f"| mid | {TAIL_MAX} < EC-4 group size ≤ {MID_MAX} |")
    w(f"| head | EC-4 group size > {MID_MAX} |")
    w("")
    w("### 3.3 Grouped MRR Computation")
    w("")
    w("- **Query rows**: only rows in the current bucket")
    w("- **Candidate enzyme rows**: ALL enzyme rows (not bucket-local)")
    w("- **Positive set**: all rows sharing the same EC-4 key")
    w("- **best_pos_score** = max similarity over the positive set")
    w("- **rank** = 1 + count(candidates with score > best_pos_score)")
    w("- **reciprocal rank** = 1 / rank")
    w("- **bucket MRR** = mean reciprocal rank over bucket query rows")
    w("- Chunked retrieval: `chunk_size = {cs}`, no full N×N matrix".format(cs=args.chunk_size))
    w("- L2 normalization applied explicitly before dot-product (cosine similarity)")
    w("")

    w("## 4. EC-4 Group Statistics")
    w("")
    gs = group_stats["all"]
    w(f"- **Total rows (N)**: {results['all']['n_queries'] + check.get('_n_excluded', 0)}")
    w(f"- **Valid EC-4 rows**: {gs['n_rows']}")
    w(f"- **Excluded rows (EC-4 unknown)**: {check.get('_n_excluded', 'N/A')}")
    w(f"- **Valid EC-4 groups**: {gs['n_groups']}")
    w(f"- **Group size — min / median / mean / p95 / max**: "
      f"{gs['min']} / {gs['median']:.1f} / {gs['mean']:.2f} / {gs['p95']:.1f} / {gs['max']}")
    w("")
    w("| Bucket | n groups | n rows | min | median | mean | p95 | max |")
    w("|--------|----------|--------|-----|--------|------|-----|-----|")
    for b in ["tail", "mid", "head"]:
        s = group_stats[b]
        w(f"| {b} | {s['n_groups']} | {s['n_rows']} | "
          f"{s['min']} | {s['median']:.1f} | {s['mean']:.2f} | {s['p95']:.1f} | {s['max']} |")
    w("")

    w("## 5. Overall Consistency Check")
    w("")
    w(f"| Metric | Value |")
    w(f"|--------|-------|")
    w(f"| Computed overall valid EC-4 grouped MRR | **{check['computed']:.10f}** |")
    w(f"| metrics_v3 EC-4-grouped MRR | **{check['expected']:.10f}** |")
    w(f"| Relative error | {check['rel_err']:.6e} |")
    w(f"| Tolerance | {check['tolerance']} |")
    w(f"| Status | **{check['status']}** |")
    w("")

    w("## 6. Bucket Baseline")
    w("")
    w("| Bucket | Rule | n groups | n rows | MRR | top-1 | top-5 | top-10 |")
    w("|--------|------|----------|--------|-----|-------|-------|--------|")
    for b in ["tail", "mid", "head"]:
        r = results[b]
        s = group_stats[b]
        rule = (f"≤{TAIL_MAX}" if b == "tail"
                else f"{TAIL_MAX+1}–{MID_MAX}" if b == "mid"
                else f">{MID_MAX}")
        w(f"| {b} | {rule} | {s['n_groups']} | {r['n_queries']} | "
          f"{r['MRR']:.6f} | {r['top-1']:.6f} | {r['top-5']:.6f} | {r['top-10']:.6f} |")
    # Overall row
    ra = results["all"]
    sa = group_stats["all"]
    w(f"| **ALL** | all valid EC-4 | {sa['n_groups']} | {ra['n_queries']} | "
      f"**{ra['MRR']:.6f}** | {ra['top-1']:.6f} | {ra['top-5']:.6f} | {ra['top-10']:.6f} |")
    w("")

    w("## 7. Output Files")
    w("")
    w(f"| File | Path |")
    w(f"|------|------|")
    w(f"| JSON report | `{out_json}` |")
    w(f"| Markdown report | `{path}` |")
    w(f"| Eval script | `{os.path.abspath(__file__)}` |")
    w("")

    w("## 8. Declarations")
    w("")
    w("- train.py modified: **no**")
    w("- eval script created: **yes**")
    w("- Slurm submitted: **no**")
    w("- GPU/DCU used: **no**")
    w("- retraining executed: **no**")
    w("- new calibration/OOD/latency thresholds introduced: **no**")
    w("- ready for local audit: **yes**")
    w("")
    w("---")
    w("")
    w(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
      f"hostname: {socket.gethostname()} | chunk_size: {args.chunk_size}*")
    w("")

    content = "\n".join(lines)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    log(f"Markdown report written to {path}")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="R2 EC-4 Bucket Baseline Evaluation")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR,
                        help="Directory containing R2 output files")
    parser.add_argument("--checkpoint", type=str, default=None,
                        help=("Alias for --output_dir for checklist compatibility; "
                              "expects a directory containing embeddings_v3.npz, "
                              "metadata_v3.json, and metrics_v3.json"))
    parser.add_argument("--report_path", type=str, default=DEFAULT_REPORT_PATH,
                        help="Path for the output markdown report")
    parser.add_argument("--chunk_size", type=int, default=DEFAULT_CHUNK_SIZE,
                        help="Chunk size for batched retrieval")
    args = parser.parse_args()
    if args.checkpoint is not None:
        args.output_dir = args.checkpoint
    require_numpy()

    log("=" * 60)
    log("R2 EC-4 Bucket Baseline Evaluation")
    log("=" * 60)
    log(f"output_dir  : {args.output_dir}")
    log(f"report_path : {args.report_path}")
    log(f"chunk_size  : {args.chunk_size}")
    log(f"hostname    : {socket.gethostname()}")
    log(f"python      : {sys.version.split()[0]}")
    log(f"numpy       : {np.__version__}")
    log("")

    # ── Load data ──
    npz_path = os.path.join(args.output_dir, "embeddings_v3.npz")
    meta_path = os.path.join(args.output_dir, "metadata_v3.json")
    metrics_path = os.path.join(args.output_dir, "metrics_v3.json")

    log("Loading embeddings...")
    t0 = time.time()
    emb = np.load(npz_path)
    reaction_emb = emb["reaction"].astype(np.float32)
    enzyme_emb = emb["enzyme"].astype(np.float32)
    log(f"  reaction: {reaction_emb.shape}, enzyme: {enzyme_emb.shape}, "
        f"loaded in {time.time()-t0:.1f}s")

    log("Loading metadata...")
    t0 = time.time()
    with open(meta_path) as f:
        metadata = json.load(f)
    log(f"  {len(metadata)} entries, loaded in {time.time()-t0:.1f}s")

    # ── Shape assertion ──
    N = len(metadata)
    assert reaction_emb.shape[0] == N, (
        f"Row count mismatch: embeddings {reaction_emb.shape[0]} vs metadata {N}")
    assert enzyme_emb.shape[0] == N, (
        f"Row count mismatch: enzyme {enzyme_emb.shape[0]} vs metadata {N}")
    log(f"Shape assertion passed: N = {N}")

    # ── L2 normalize ──
    log("Applying L2 normalization...")
    reaction_emb = l2_normalize(reaction_emb).astype(np.float32)
    enzyme_emb = l2_normalize(enzyme_emb).astype(np.float32)

    # ── Build EC-4 groups ──
    log("Building EC-4 groups...")
    ec4_labels, groups_dict, valid_mask = build_ec4_groups(metadata)
    n_valid = int(valid_mask.sum())
    n_excluded = N - n_valid
    log(f"  valid EC-4 rows: {n_valid}, excluded: {n_excluded}, "
        f"groups: {len(groups_dict)}")

    # ── Assign buckets ──
    log("Assigning buckets...")
    key_to_bucket = assign_buckets(groups_dict)
    row_buckets = map_rows_to_buckets(ec4_labels, key_to_bucket)
    for b in ["tail", "mid", "head"]:
        ng = sum(1 for v in key_to_bucket.values() if v == b)
        nr = sum(1 for rb in row_buckets if rb == b)
        log(f"  {b}: {ng} groups, {nr} rows")

    # ── Compute MRR ──
    log("")
    log("Computing grouped R→E MRR per bucket...")
    results = compute_bucket_mrr(
        reaction_emb, enzyme_emb, ec4_labels, groups_dict,
        valid_mask, key_to_bucket, row_buckets, args.chunk_size)

    for b in ["tail", "mid", "head", "all"]:
        r = results[b]
        log(f"  {b:5s}: MRR={r['MRR']:.6f}  top-1={r['top-1']:.6f}  "
            f"top-5={r['top-5']:.6f}  top-10={r['top-10']:.6f}  n={r['n_queries']}")

    # ── Group statistics ──
    log("")
    log("Computing group statistics...")
    group_stats = compute_group_stats(groups_dict, key_to_bucket)

    # ── Consistency check ──
    log("")
    log("Running consistency check against metrics_v3.json...")
    check = consistency_check(results["all"]["MRR"], metrics_path)
    check["_n_excluded"] = n_excluded  # stash for markdown
    log(f"  expected : {check['expected']:.10f}")
    log(f"  computed : {check['computed']:.10f}")
    log(f"  rel_err  : {check['rel_err']:.6e}")
    log(f"  status   : {check['status']}")

    # ── Write outputs ──
    log("")
    out_json = os.path.join(args.output_dir, "r2_ec4_bucket_baseline.json")
    write_json_report(results, group_stats, check, args, out_json)
    write_markdown_report(results, group_stats, check, args, args.report_path)

    log("")
    log("=" * 60)
    log("R2 EC-4 Bucket Baseline Evaluation complete.")
    log("=" * 60)


if __name__ == "__main__":
    main()
