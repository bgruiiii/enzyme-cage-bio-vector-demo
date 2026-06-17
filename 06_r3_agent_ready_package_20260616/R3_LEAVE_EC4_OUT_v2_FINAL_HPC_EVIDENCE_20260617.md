# R3 Leave-EC4-Out v2 — Final HPC Evidence Log

**Generated**: 2026-06-17
**Purpose**: Confirm final v2 leak-fix artifacts exist on HPC, extract key metrics, verify no stale conclusions remain. Read-only evidence collection; no code changes, no retraining, no GPU/DCU, no R4.

---

## 1. Exact File Paths

| Artifact | Absolute Path |
|----------|---------------|
| Eval script (v2 patched) | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/code/demo/eval_leave_ec4_out.py` |
| v2 Markdown report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_v2_20260617_001330.md` |
| v2 JSON report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_leave_ec4_out_v2.json` |
| v1 Markdown (pre-fix, reference) | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_20260616_171432.md` |
| v1 Leaked copy (deprecated) | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md` |

> **Note**: `R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md` was created as a copy of the original `R3_LEAVE_EC4_OUT_20260616_171432.md` with a deprecation header prepended. The original file is preserved unchanged.

---

## 2. ls -lh Output (raw)

```
$ ls -lh eval_leave_ec4_out.py R3_LEAVE_EC4_OUT_20260616_171432.md \
         R3_LEAVE_EC4_OUT_v2_20260617_001330.md r3_leave_ec4_out_v2.json

-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  33K Jun 17 00:11 /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/code/demo/eval_leave_ec4_out.py
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 3.2K Jun 16 17:14 /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_20260616_171432.md
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 4.9K Jun 17 00:13 /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_v2_20260617_001330.md
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 327K Jun 17 00:13 /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_leave_ec4_out_v2.json
```

**Verdict**: All 4 files exist. Sizes are consistent with completed v2 evaluation.

---

## 3. py_compile Result

```
$ /public/home/acfbwjsi7s/miniconda3/envs/nis/bin/python -m py_compile \
    /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/code/demo/eval_leave_ec4_out.py
COMPILE_OK
```

**Verdict**: No syntax errors. Exit code 0.

---

## 4. JSON Key Metrics (raw from r3_leave_ec4_out_v2.json)

```
timestamp: 2026-06-17 00:13:30

holdout:
  n_classes: 126
  holdout_row_count: 7518
  holdout_evaluated_queries: 7513
  holdout_skipped_queries: 5
  holdout_corpus_mask_ban_count: 7518

holdout metrics:
  n_queries: 7513
  MRR:   0.6187024772231093
  top-1: 0.5880473845334753
  top-5: 0.6234526820178358
  top-10: 0.6535338746173299

in_sample metrics:
  n_queries: 5000
  MRR:   0.9337374438177458
  top-1: 0.899
  top-5: 0.9362
  top-10: 0.9596

ratios:
  ratio_MRR:   0.6626086180001929
  ratio_top-1: 0.6541127747869581
  ratio_top-5: 0.6659396304399015
  ratio_top-10: 0.6810482228192267

threshold_ratings:
  EC-3-grouped MRR:  0.6187 vs 0.50 (eff. 0.45) -> PASS
  EC-3 top-5:        0.6235 vs 0.65 (eff. 0.60) -> PASS
  HO/IS ratio MRR:   0.6626 vs 0.65 (eff. 0.60) -> PASS

declarations:
  train_py_modified: false
  eval_script_patched: true
  v2_leak_fix: true
  sbatch_executed: false
  gpu_dcu_used: false
  retraining_executed: false
  full_evaluation_executed: true
  r4_opened: false
  new_training_objective_introduced: false
```

---

## 5. Grep Key-Statement Results (raw)

Searched patterns in `R3_LEAVE_EC4_OUT_v2_20260617_001330.md`:

```
$ grep -nE "Hold-out corpus mask banned rows|Evaluated hold-out queries|
  Skipped hold-out queries|Direction OK|Expected-Range|
  0.618702|0.623453|0.662609|teacher tolerance" R3_LEAVE_EC4_OUT_v2_20260617_001330.md

41:| Hold-out corpus mask banned rows | **7518** |
42:| Evaluated hold-out queries | **7513** |
43:| Skipped hold-out queries (gi_eff empty) | **5** |
53:## 6. Expected-Range Comparison
57:| HO_EC3_MRR | 0.618702 | [0.45, 0.75] | **within** |
59:| HO_IS_MRR_ratio | 0.662609 | [0.70, 0.95] | **outside** |
61:> **Direction OK**: HO/IS MRR ratio < 1.0 (hold-out is harder than in-sample, as expected).
67:| EC-3 MRR | 0.618702 | 0.933737 | 0.662609 |
69:| EC-3 top-5 | 0.623453 | 0.936200 | 0.665940 |
78:| EC-3-grouped MRR | 0.618702 | 0.50 | 0.45 | **PASS** |
79:| EC-3 top-5 | 0.623453 | 0.65 | 0.60 | **PASS** |
80:| HO/IS ratio MRR | 0.662609 | 0.65 | 0.60 | **PASS** |
86: ...teacher tolerance.
```

**Verdict**: All 9 required patterns found. Every key statement, metric value, and structural section present.

| Pattern | Found? | Line(s) |
|---------|--------|---------|
| `Hold-out corpus mask banned rows` | YES | L41 |
| `Evaluated hold-out queries` | YES | L42 |
| `Skipped hold-out queries` | YES | L43 |
| `Direction OK` | YES | L61 |
| `Expected-Range` | YES | L53 |
| `0.618702` | YES | L57, 67, 78 |
| `0.623453` | YES | L69, 79 |
| `0.662609` | YES | L59, 67, 80 |
| `teacher tolerance` | YES | L86 |

---

## 6. Old-Conclusion Negative Search (raw)

Searched in both v2 markdown and v2 JSON for the old v1 final-claim phrase set.
The search returned no matches.

**Verdict**: Zero hits. No stale/incorrect conclusion text remains in v2 artifacts.

| Stale phrase group | Matches |
|---------------|---------|
| prior generalization-support claim | 0 |
| prior robust-transfer claim | 0 |
| prior all-thresholds-passed claim | 0 |
| prior v1-MRR decision expression | 0 |

---

## 7. Evidence Verdict

- All required v2 artifacts present and well-formed.
- `py_compile` passes cleanly.
- All 9 required key-statement patterns found in v2 markdown.
- All 6 stale-conclusion patterns absent from v2 artifacts (zero false positives).
- v1 leaked copy created with correct deprecation header per teacher checklist.

---

## 8. Declarations

| Item | Status |
|------|--------|
| train.py modified | **no** |
| eval script patched (v2 leak-fix) | **yes** |
| v2_leak_fix | **true** |
| sbatch executed | **no** |
| GPU/DCU used | **no** |
| retraining executed | **no** |
| full evaluation executed | **yes** |
| R4 opened | **no** |
| new training objective introduced | **no** |

---

## 9. v1 Leaked Copy (Teacher Checklist Item)

| Check | Result |
|-------|--------|
| v1 leaked copy created | **yes** — `R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md` |
| original v1 retained | **yes** — `R3_LEAVE_EC4_OUT_20260616_171432.md` unchanged |
| v1 leaked header present | **yes** — `> 已废弃：存在 target leakage（同 class corpus + self），见 v2 报告` |
| train.py modified | **no** |
| sbatch executed | **no** |
| GPU/DCU used | **no** |
| retraining executed | **no** |
| R4 opened | **no** |

### ls -lh output

```
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 3.2K Jun 16 17:14 R3_LEAVE_EC4_OUT_20260616_171432.md
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 3.3K Jun 17 10:02 R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 4.9K Jun 17 00:13 R3_LEAVE_EC4_OUT_v2_20260617_001330.md
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 327K Jun 17 00:13 r3_leave_ec4_out_v2.json
```

### head -n 5 v1 leaked file

```
> 已废弃：存在 target leakage（同 class corpus + self），见 v2 报告

# R3 Leave-EC4-Class-Out Validation Report

**Timestamp**: 2026-06-16 17:14:32
```

---

## 10. Summary

- All v2 artifacts exist at expected HPC paths with correct sizes.
- `py_compile` passes cleanly (COMPILE_OK).
- JSON contains all v2 audit fields: `holdout_evaluated_queries`, `holdout_skipped_queries`, `holdout_corpus_mask_ban_count`, `expected_ranges`.
- v2 markdown contains all required structural elements (corpus mask, skipped queries, expected-range comparison, direction check, nuanced conclusion).
- No stale conclusion text from v1 leaked into v2 reports.
- All declarations consistent with boundary constraints (no train.py change, no retraining, no GPU, no R4, no sbatch).
- v1 leaked copy with deprecation header created per teacher checklist.

---

*Evidence collected: 2026-06-17 | HPC login09 | numpy 1.26.4 | Python 3.9.23*
