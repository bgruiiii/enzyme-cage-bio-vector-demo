#!/usr/bin/env python3
"""
R3 Leave-EC4-Class-Out Validation

Zero-GPU evaluation using saved R3 embeddings only.
Holds out a fraction of EC-4 classes and measures EC-3-grouped R→E retrieval
on the held-out rows vs. an in-sample 5 000-row subset.

Reads ONLY:
  - metadata_v3.json
  - embeddings_v3.npz

Does NOT load model_v3.pt, does NOT import train.py, does NOT use torch.

Usage:
    python eval_leave_ec4_out.py \\
        --output_dir /path/to/r3_outputs \\
        --seed 20260616 \\
        --holdout_ratio 0.05
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

import numpy as np

# ──────────────────────────────────────────────────────────────────────
# Constants / Thresholds
# ──────────────────────────────────────────────────────────────────────
DEFAULT_CHUNK_SIZE = 2048
IN_SAMPLE_SUBSET_SIZE = 5000

THRESHOLDS = [
    # (display_label,  source,    lookup_key,  threshold)
    ("EC-3-grouped MRR", "holdout", "MRR",        0.80),
    ("EC-3 top-1",       "holdout", "top-1",      0.70),
    ("EC-3 top-5",       "holdout", "top-5",      0.85),
    ("EC-3 top-10",      "holdout", "top-10",     0.92),
    ("HO/IS ratio MRR",  "ratio",   "ratio_MRR",  0.85),
]
TOLERANCE = 0.05


# ──────────────────────────────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def parse_ec4(ec_str):
    """Strict EC-4 parser.

    Returns 'a.b.c.d' when the first 4 dot-separated segments all pass
    int(); otherwise returns None.
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


def parse_ec3(ec_str):
    """Strict EC-3 parser — matches train.py _parse_ec3.

    Returns 'a.b.c' when the first 3 dot-separated segments all pass
    int(); otherwise returns None.
    """
    if not ec_str or not isinstance(ec_str, str):
        return None
    s = ec_str.strip()
    if s in ("", "unknown", "-"):
        return None
    parts = s.split(".")
    if len(parts) < 3:
        return None
    try:
        for i in range(3):
            int(parts[i])
    except ValueError:
        return None
    return f"{parts[0]}.{parts[1]}.{parts[2]}"


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
# Core: Chunked EC-3-Grouped Retrieval
# ──────────────────────────────────────────────────────────────────────
def compute_ec3_grouped_metrics(query_emb, corpus_emb, ec3_labels_query,
                                 ec3_groups_arr, chunk_size, ks=(1, 5, 10),
                                 ec4_labels_query=None):
    """Compute EC-3-grouped R->E retrieval metrics over a set of queries.

    Args:
        query_emb: (n_query, D) reaction embeddings (L2-normalized).
        corpus_emb: (N, D) enzyme embeddings (L2-normalized).
        ec3_labels_query: list of EC-3 strings, one per query row.
        ec3_groups_arr: dict[ec3_key -> np.ndarray[int]] mapping each EC-3
            class to its member indices in the *corpus* (all rows).
        chunk_size: int
        ks: tuple of k values for top-k.
        ec4_labels_query: optional list of EC-4 strings for per-EC4-class
            summary (hold-out only).  Length must match n_query.

    Returns:
        dict with keys:
            n_queries, MRR, top-1, top-5, top-10  (aggregate)
            rank_list: list[int]  — per-query rank (0 for skipped)
            per_ec4_class: dict  — per-EC4-class metrics (only if ec4_labels_query given)
    """
    N = corpus_emb.shape[0]
    n_query = query_emb.shape[0]
    max_k = max(ks)

    accum = {"rr_sum": 0.0, "top1": 0, "top5": 0, "top10": 0, "n": 0}
    ranks = [0] * n_query  # 0 = skipped / invalid

    # Per-EC4-class accumulators
    ec4_accum = {}
    if ec4_labels_query is not None:
        for ec4 in ec4_labels_query:
            if ec4 is not None and ec4 not in ec4_accum:
                ec4_accum[ec4] = {"rr_sum": 0.0, "top1": 0, "top5": 0,
                                   "top10": 0, "n": 0}

    n_chunks = (n_query + chunk_size - 1) // chunk_size
    t0 = time.time()

    for ci, start in enumerate(range(0, n_query, chunk_size)):
        end = min(start + chunk_size, n_query)
        sim_chunk = query_emb[start:end] @ corpus_emb.T   # (chunk, N)

        for local_i in range(end - start):
            global_i = start + local_i
            my_ec3 = ec3_labels_query[global_i]
            if my_ec3 is None:
                continue

            gi = ec3_groups_arr.get(my_ec3)
            if gi is None or len(gi) == 0:
                continue

            s = sim_chunk[local_i]  # (N,) cosine scores

            # Grouped MRR
            best_pos_score = float(np.max(s[gi]))
            rank = int(np.sum(s > best_pos_score)) + 1
            rr = 1.0 / rank
            ranks[global_i] = rank
            accum["rr_sum"] += rr

            # Top-k
            k_eff = min(max_k, len(s))
            topk_unsorted = np.argpartition(-s, k_eff - 1)[:k_eff]
            topk_idx = topk_unsorted[np.argsort(-s[topk_unsorted])]
            gset = set(gi.tolist())
            t1_hit = int(bool(set(topk_idx[:1].tolist()) & gset))
            t5_hit = int(bool(set(topk_idx[:5].tolist()) & gset))
            t10_hit = int(bool(set(topk_idx[:10].tolist()) & gset))
            accum["top1"]  += t1_hit
            accum["top5"]  += t5_hit
            accum["top10"] += t10_hit
            accum["n"] += 1

            # Per-EC4-class accum
            if ec4_labels_query is not None:
                my_ec4 = ec4_labels_query[global_i]
                if my_ec4 is not None and my_ec4 in ec4_accum:
                    ea = ec4_accum[my_ec4]
                    ea["rr_sum"] += rr
                    ea["top1"]  += t1_hit
                    ea["top5"]  += t5_hit
                    ea["top10"] += t10_hit
                    ea["n"] += 1

        del sim_chunk
        if (ci + 1) % 10 == 0 or ci == n_chunks - 1:
            elapsed = time.time() - t0
            log(f"  chunk {ci+1}/{n_chunks} done, elapsed={elapsed:.1f}s")

    n = accum["n"]
    if n == 0:
        result = {"n_queries": 0, "MRR": 0.0,
                  "top-1": 0.0, "top-5": 0.0, "top-10": 0.0,
                  "rank_list": ranks}
    else:
        result = {
            "n_queries": n,
            "MRR":   accum["rr_sum"] / n,
            "top-1":  accum["top1"] / n,
            "top-5":  accum["top5"] / n,
            "top-10": accum["top10"] / n,
            "rank_list": ranks,
        }

    # Build per-EC4-class summary
    per_ec4_class = None
    if ec4_labels_query is not None:
        per_ec4_class = {}
        for ec4_key in sorted(ec4_accum.keys()):
            ea = ec4_accum[ec4_key]
            en = ea["n"]
            if en > 0:
                per_ec4_class[ec4_key] = {
                    "n_queries": en,
                    "MRR":   ea["rr_sum"] / en,
                    "top-1":  ea["top1"] / en,
                    "top-5":  ea["top5"] / en,
                    "top-10": ea["top10"] / en,
                }
            else:
                per_ec4_class[ec4_key] = {
                    "n_queries": 0,
                    "MRR": 0.0, "top-1": 0.0, "top-5": 0.0, "top-10": 0.0,
                }
    result["per_ec4_class"] = per_ec4_class
    return result


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="R3 Leave-EC4-Class-Out Validation (zero-GPU, numpy only)")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="Directory containing R3 output files "
                             "(metadata_v3.json, embeddings_v3.npz)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for hold-out selection (default: 42)")
    parser.add_argument("--holdout_ratio", type=float, default=0.05,
                        help="Fraction of EC-4 classes to hold out (default: 0.05)")
    parser.add_argument("--chunk_size", type=int, default=DEFAULT_CHUNK_SIZE,
                        help=f"Chunk size for batched retrieval (default: {DEFAULT_CHUNK_SIZE})")
    args = parser.parse_args()

    log("=" * 60)
    log("R3 Leave-EC4-Class-Out Validation")
    log("=" * 60)
    log(f"output_dir   : {args.output_dir}")
    log(f"seed         : {args.seed}")
    log(f"holdout_ratio: {args.holdout_ratio}")
    log(f"chunk_size   : {args.chunk_size}")
    log(f"hostname     : {socket.gethostname()}")
    log(f"python       : {sys.version.split()[0]}")
    log(f"numpy        : {np.__version__}")
    log("")

    # ── Paths ──
    npz_path  = os.path.join(args.output_dir, "embeddings_v3.npz")
    meta_path = os.path.join(args.output_dir, "metadata_v3.json")

    for p in (npz_path, meta_path):
        if not os.path.isfile(p):
            raise FileNotFoundError(f"Required file not found: {p}")

    # ── Load data ──
    log("Loading embeddings...")
    t0 = time.time()
    emb = np.load(npz_path)
    reaction_emb = emb["reaction"].astype(np.float32)
    enzyme_emb   = emb["enzyme"].astype(np.float32)
    log(f"  reaction: {reaction_emb.shape}, enzyme: {enzyme_emb.shape}, "
        f"loaded in {time.time()-t0:.1f}s")

    log("Loading metadata...")
    t0 = time.time()
    with open(meta_path) as f:
        metadata = json.load(f)
    log(f"  {len(metadata)} entries, loaded in {time.time()-t0:.1f}s")

    N = len(metadata)
    assert reaction_emb.shape[0] == N, \
        f"Row count mismatch: reaction {reaction_emb.shape[0]} vs metadata {N}"
    assert enzyme_emb.shape[0] == N, \
        f"Row count mismatch: enzyme {enzyme_emb.shape[0]} vs metadata {N}"
    log(f"Shape assertion passed: N = {N}")

    # ── L2 normalize ──
    log("Applying L2 normalization...")
    reaction_emb = l2_normalize(reaction_emb).astype(np.float32)
    enzyme_emb   = l2_normalize(enzyme_emb).astype(np.float32)

    # ── Parse EC labels ──
    log("Parsing EC labels...")
    ec4_labels = []
    ec3_labels = []
    ec4_groups = defaultdict(list)
    ec3_groups = defaultdict(list)

    for i in range(N):
        ec_str = metadata[i].get("ec_number", "")
        ec4 = parse_ec4(ec_str)
        ec3 = parse_ec3(ec_str)
        ec4_labels.append(ec4)
        ec3_labels.append(ec3)
        if ec4 is not None:
            ec4_groups[ec4].append(i)
        if ec3 is not None:
            ec3_groups[ec3].append(i)

    ec4_groups = {k: np.array(v, dtype=np.int64) for k, v in ec4_groups.items()}
    ec3_groups_arr = {k: np.array(v, dtype=np.int64) for k, v in ec3_groups.items()}

    n_valid_ec4 = sum(1 for x in ec4_labels if x is not None)
    n_valid_ec3 = sum(1 for x in ec3_labels if x is not None)
    log(f"  valid EC-4 rows: {n_valid_ec4}, unique EC-4 classes: {len(ec4_groups)}")
    log(f"  valid EC-3 rows: {n_valid_ec3}, unique EC-3 classes: {len(ec3_groups)}")

    # ── Select hold-out EC-4 classes ──
    log("")
    log("Selecting hold-out EC-4 classes...")
    all_ec4_classes = sorted(ec4_groups.keys())
    rng = np.random.RandomState(args.seed)
    n_holdout_classes = max(1, int(round(len(all_ec4_classes) * args.holdout_ratio)))
    holdout_class_indices = rng.choice(
        len(all_ec4_classes), size=n_holdout_classes, replace=False)
    holdout_class_indices.sort()
    holdout_classes = [all_ec4_classes[i] for i in holdout_class_indices]
    log(f"  hold-out EC-4 classes: {len(holdout_classes)} / {len(all_ec4_classes)}")

    # ── Hold-out row mask ──
    holdout_class_set = set(holdout_classes)
    holdout_row_indices = np.array(
        [i for i in range(N) if ec4_labels[i] is not None
         and ec4_labels[i] in holdout_class_set],
        dtype=np.int64)
    holdout_row_set = set(holdout_row_indices.tolist())
    in_sample_row_indices = np.array(
        [i for i in range(N) if i not in holdout_row_set
         and ec3_labels[i] is not None],
        dtype=np.int64)

    n_holdout_rows = len(holdout_row_indices)
    n_in_sample = len(in_sample_row_indices)
    holdout_pct = 100.0 * n_holdout_rows / N if N > 0 else 0.0
    log(f"  hold-out rows: {n_holdout_rows} ({holdout_pct:.2f}%)")
    log(f"  in-sample rows: {n_in_sample}")

    # ── In-sample 5 000-row subset ──
    log("")
    log(f"Sampling in-sample subset (target {IN_SAMPLE_SUBSET_SIZE})...")
    actual_subset_size = min(IN_SAMPLE_SUBSET_SIZE, n_in_sample)
    rng2 = np.random.RandomState(args.seed)
    subset_pick = rng2.choice(in_sample_row_indices, size=actual_subset_size,
                               replace=False)
    subset_pick.sort()
    log(f"  in-sample subset size: {actual_subset_size}")

    # ── Hold-out EC-3 grouped retrieval ──
    log("")
    log("=" * 60)
    log("Computing EC-3-grouped retrieval for HOLD-OUT rows...")
    log("=" * 60)
    ho_ec3_labels = [ec3_labels[i] for i in holdout_row_indices]
    ho_ec4_labels = [ec4_labels[i] for i in holdout_row_indices]
    ho_reaction = reaction_emb[holdout_row_indices]
    ho_metrics = compute_ec3_grouped_metrics(
        ho_reaction, enzyme_emb, ho_ec3_labels, ec3_groups_arr,
        args.chunk_size, ec4_labels_query=ho_ec4_labels)
    for k, v in ho_metrics.items():
        if k not in ("rank_list", "per_ec4_class"):
            log(f"  hold-out {k}: {v}")

    # ── In-sample subset EC-3 grouped retrieval ──
    log("")
    log("=" * 60)
    log("Computing EC-3-grouped retrieval for IN-SAMPLE subset...")
    log("=" * 60)
    is_ec3_labels = [ec3_labels[i] for i in subset_pick]
    is_reaction = reaction_emb[subset_pick]
    is_metrics = compute_ec3_grouped_metrics(
        is_reaction, enzyme_emb, is_ec3_labels, ec3_groups_arr,
        args.chunk_size)
    for k, v in is_metrics.items():
        if k not in ("rank_list", "per_ec4_class"):
            log(f"  in-sample {k}: {v}")

    # ── Ratios ──
    log("")
    log("Computing hold-out / in-sample ratios...")
    ratios = {}
    for metric_key in ("MRR", "top-1", "top-5", "top-10"):
        ho_val = ho_metrics[metric_key]
        is_val = is_metrics[metric_key]
        ratio = ho_val / is_val if is_val > 0 else float("inf")
        ratios[f"ratio_{metric_key}"] = ratio
        log(f"  ratio_{metric_key}: {ratio:.6f}  "
            f"(hold-out={ho_val:.6f}, in-sample={is_val:.6f})")

    # ── Threshold ratings ──
    log("")
    log("Evaluating against teacher thresholds...")
    threshold_ratings = {}
    for label, source, lookup_key, threshold in THRESHOLDS:
        if source == "ratio":
            value = ratios.get(lookup_key, 0.0)
        else:
            value = ho_metrics.get(lookup_key, 0.0)
        passed = value >= (threshold - TOLERANCE)
        rating = "PASS" if passed else "FAIL"
        threshold_ratings[label] = {
            "value": value,
            "threshold": threshold,
            "tolerance": TOLERANCE,
            "effective_threshold": threshold - TOLERANCE,
            "rating": rating,
        }
        log(f"  {label}: {value:.6f} vs {threshold:.2f} "
            f"(eff. {threshold - TOLERANCE:.2f}) -> {rating}")

    # ── Qualitative conclusion ──
    n_pass = sum(1 for v in threshold_ratings.values() if v["rating"] == "PASS")
    n_total = len(threshold_ratings)
    all_pass = n_pass == n_total
    if all_pass:
        conclusion = (
            "All hold-out metrics meet or exceed teacher thresholds "
            "(with +/-0.05 tolerance). The hold-out / in-sample ratio "
            "supports generalization. R3 embeddings demonstrate robust "
            "cross-EC-4-class transfer.")
    else:
        failed = [k for k, v in threshold_ratings.items() if v["rating"] == "FAIL"]
        conclusion = (
            f"{n_pass}/{n_total} thresholds passed. "
            f"Failed metrics: {', '.join(failed)}. "
            f"Generalization may be limited for held-out EC-4 classes. "
            f"Further investigation recommended.")

    log("")
    log(f"Conclusion: {conclusion}")

    # ── Write JSON ──
    log("")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(args.output_dir, "r3_leave_ec4_out.json")
    json_report = {
        "task": "R3 Leave-EC4-Class-Out Validation",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "seed": args.seed,
            "holdout_ratio": args.holdout_ratio,
            "chunk_size": args.chunk_size,
            "in_sample_subset_target": IN_SAMPLE_SUBSET_SIZE,
            "in_sample_subset_actual": actual_subset_size,
        },
        "input_paths": {
            "embeddings": npz_path,
            "metadata": meta_path,
        },
        "dataset": {
            "total_rows": N,
            "valid_ec4_rows": n_valid_ec4,
            "valid_ec3_rows": n_valid_ec3,
            "unique_ec4_classes": len(ec4_groups),
            "unique_ec3_classes": len(ec3_groups),
        },
        "holdout": {
            "n_classes": len(holdout_classes),
            "holdout_class_list": holdout_classes,
            "holdout_row_count": n_holdout_rows,
            "holdout_row_percentage": holdout_pct,
            "holdout_row_indices": holdout_row_indices.tolist(),
        },
        "in_sample": {
            "n_in_sample_total": n_in_sample,
            "subset_size": actual_subset_size,
            "subset_row_indices": subset_pick.tolist(),
        },
        "metrics": {
            "holdout": to_jsonable(ho_metrics),
            "in_sample": to_jsonable(is_metrics),
        },
        "ratios": to_jsonable(ratios),
        "threshold_ratings": to_jsonable(threshold_ratings),
        "conclusion": conclusion,
        "environment": {
            "hostname": socket.gethostname(),
            "python": sys.version,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "declarations": {
            "train_py_modified": False,
            "eval_script_created": True,
            "sbatch_executed": False,
            "gpu_dcu_used": False,
            "retraining_executed": False,
            "full_evaluation_executed": True,
            "new_training_objective_introduced": False,
        },
    }
    with open(json_path, "w") as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    log(f"JSON report written to {json_path}")

    # ── Write Markdown ──
    md_path = os.path.join(args.output_dir,
                            f"R3_LEAVE_EC4_OUT_{timestamp}.md")
    lines = []
    w = lines.append

    w("# R3 Leave-EC4-Class-Out Validation Report")
    w("")
    w(f"**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    w(f"**Hostname**: {socket.gethostname()}")
    w("")

    w("## 1. Purpose")
    w("")
    w("This report documents the **R3 Leave-EC4-Class-Out validation** — a "
      "zero-GPU evaluation using only saved R3 embeddings. A fraction of EC-4 "
      "classes are held out, and EC-3-grouped R->E retrieval performance is "
      "measured on the held-out rows and compared against an in-sample 5 000-row "
      "subset. **No model loading, no training, no torch.**")
    w("")

    w("## 2. Configuration")
    w("")
    w("| Parameter | Value |")
    w("|-----------|-------|")
    w(f"| output_dir | `{args.output_dir}` |")
    w(f"| seed | {args.seed} |")
    w(f"| holdout_ratio | {args.holdout_ratio} |")
    w(f"| chunk_size | {args.chunk_size} |")
    w(f"| in-sample subset target | {IN_SAMPLE_SUBSET_SIZE} |")
    w(f"| in-sample subset actual | {actual_subset_size} |")
    w("")

    w("## 3. Dataset Summary")
    w("")
    w("| Statistic | Value |")
    w("|-----------|-------|")
    w(f"| Total rows (N) | {N} |")
    w(f"| Valid EC-4 rows | {n_valid_ec4} |")
    w(f"| Valid EC-3 rows | {n_valid_ec3} |")
    w(f"| Unique EC-4 classes | {len(ec4_groups)} |")
    w(f"| Unique EC-3 classes | {len(ec3_groups)} |")
    w("")

    w("## 4. Hold-Out Summary")
    w("")
    w("| Statistic | Value |")
    w("|-----------|-------|")
    w(f"| Hold-out EC-4 class count | **{len(holdout_classes)}** |")
    w(f"| Hold-out row count | **{n_holdout_rows}** |")
    w(f"| Hold-out row percentage | **{holdout_pct:.2f}%** |")
    w(f"| In-sample rows | {n_in_sample} |")
    w(f"| In-sample subset size | {actual_subset_size} |")
    w("")

    w("## 5. Hold-Out vs In-Sample Comparison")
    w("")
    w("| Metric | Hold-Out | In-Sample (5K) | Ratio (HO/IS) |")
    w("|--------|----------|-----------------|---------------|")
    for metric_key in ("MRR", "top-1", "top-5", "top-10"):
        ho_val = ho_metrics[metric_key]
        is_val = is_metrics[metric_key]
        ratio = ratios[f"ratio_{metric_key}"]
        w(f"| EC-3 {metric_key} | {ho_val:.6f} | {is_val:.6f} | {ratio:.6f} |")
    w("")

    w("## 6. Threshold Evaluation")
    w("")
    w("Teacher thresholds (with **+/-0.05 tolerance** caveat):")
    w("")
    w("| Metric | Value | Threshold | Effective | Rating |")
    w("|--------|-------|-----------|-----------|--------|")
    for label, info in threshold_ratings.items():
        w(f"| {label} | {info['value']:.6f} | {info['threshold']:.2f} | "
          f"{info['effective_threshold']:.2f} | **{info['rating']}** |")
    w("")
    w(f"**Result: {n_pass}/{n_total} thresholds passed.**")
    w("")

    w("## 7. Qualitative Conclusion")
    w("")
    w(conclusion)
    w("")
    w("> **Teacher caveat**: thresholds allow about +/-0.05 tolerance. "
      "A metric slightly below the nominal threshold (within tolerance) "
      "is still considered acceptable.")
    w("")

    w("## 8. Output Files")
    w("")
    w("| File | Path |")
    w("|------|------|")
    w(f"| JSON report | `{json_path}` |")
    w(f"| Markdown report | `{md_path}` |")
    w(f"| Eval script | `{os.path.abspath(__file__)}` |")
    w("")

    w("## 9. Declarations")
    w("")
    w("- train.py modified: **no**")
    w("- eval script created: **yes**")
    w("- sbatch executed: **no**")
    w("- GPU/DCU used: **no**")
    w("- retraining executed: **no**")
    w("- full evaluation executed: **yes**")
    w("- new training objective introduced: **no**")
    w("")
    w("---")
    w("")
    w(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
      f"hostname: {socket.gethostname()} | numpy: {np.__version__}*")

    content = "\n".join(lines)
    with open(md_path, "w") as f:
        f.write(content)
    log(f"Markdown report written to {md_path}")

    log("")
    log("=" * 60)
    log("R3 Leave-EC4-Class-Out Validation complete.")
    log("=" * 60)


if __name__ == "__main__":
    main()
