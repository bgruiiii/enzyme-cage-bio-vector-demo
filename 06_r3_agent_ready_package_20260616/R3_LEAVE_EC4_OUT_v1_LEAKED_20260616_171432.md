> 已废弃：存在 target leakage（同 class corpus + self），见 v2 报告

# R3 Leave-EC4-Class-Out Validation Report

**Timestamp**: 2026-06-16 17:14:32
**Hostname**: login04

## 1. Purpose

This report documents the **R3 Leave-EC4-Class-Out validation** — a zero-GPU evaluation using only saved R3 embeddings. A fraction of EC-4 classes are held out, and EC-3-grouped R->E retrieval performance is measured on the held-out rows and compared against an in-sample 5 000-row subset. **No model loading, no training, no torch.**

## 2. Configuration

| Parameter | Value |
|-----------|-------|
| output_dir | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15` |
| seed | 20260616 |
| holdout_ratio | 0.05 |
| chunk_size | 2048 |
| in-sample subset target | 5000 |
| in-sample subset actual | 5000 |

## 3. Dataset Summary

| Statistic | Value |
|-----------|-------|
| Total rows (N) | 145607 |
| Valid EC-4 rows | 127847 |
| Valid EC-3 rows | 130635 |
| Unique EC-4 classes | 2524 |
| Unique EC-3 classes | 187 |

## 4. Hold-Out Summary

| Statistic | Value |
|-----------|-------|
| Hold-out EC-4 class count | **126** |
| Hold-out row count | **7518** |
| Hold-out row percentage | **5.16%** |
| In-sample rows | 123117 |
| In-sample subset size | 5000 |

## 5. Hold-Out vs In-Sample Comparison

| Metric | Hold-Out | In-Sample (5K) | Ratio (HO/IS) |
|--------|----------|-----------------|---------------|
| EC-3 MRR | 0.984791 | 0.935949 | 1.052185 |
| EC-3 top-1 | 0.966879 | 0.889600 | 1.086870 |
| EC-3 top-5 | 0.984836 | 0.937400 | 1.050604 |
| EC-3 top-10 | 0.984836 | 0.961000 | 1.024804 |

## 6. Original Threshold Evaluation (Superseded)

The table below is retained from the original v1 run for audit traceability.
It is superseded by the v2 leak-fix evaluation because v1 did not exclude same
EC-4 corpus rows or query self rows.

| Metric | Value | Threshold | Effective | Rating |
|--------|-------|-----------|-----------|--------|
| EC-3-grouped MRR | 0.984791 | 0.80 | 0.75 | superseded v1 output |
| EC-3 top-1 | 0.966879 | 0.70 | 0.65 | superseded v1 output |
| EC-3 top-5 | 0.984836 | 0.85 | 0.80 | superseded v1 output |
| EC-3 top-10 | 0.984836 | 0.92 | 0.87 | superseded v1 output |
| HO/IS ratio MRR | 1.052185 | 0.85 | 0.80 | superseded v1 output |

**Superseded v1 result:** original threshold ratings are not used as
cross-EC4-class transfer evidence.

## 7. Qualitative Conclusion

This v1 run measures row-level self-alignment under R3 embeddings, not
cross-EC4-class transfer. The HO/IS ratio is greater than `1.0`, which is the
leakage direction identified by the teacher. Use the v2 report as the final
cross-class validation.

> **Teacher caveat**: v1 is retained only as leaked audit evidence.

## 8. Output Files

| File | Path |
|------|------|
| JSON report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_leave_ec4_out.json` |
| Markdown report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/R3_LEAVE_EC4_OUT_20260616_171432.md` |
| Eval script | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/code/demo/eval_leave_ec4_out.py` |

## 9. Declarations

- train.py modified: **no**
- eval script created: **yes**
- sbatch executed: **no**
- GPU/DCU used: **no**
- retraining executed: **no**
- full evaluation executed: **yes**
- new training objective introduced: **no**

---

*Generated: 2026-06-16 17:14:32 | hostname: login04 | numpy: 1.26.4*
