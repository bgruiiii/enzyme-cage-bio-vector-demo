# R3 EC-4 Bucket Evaluation

**Date:** 2026-06-15
**R3 Job:** 115402116

---

## 1. Purpose

This report documents the **R3 EC-4 bucket evaluation**, applying the same bucket rules and eval script used for the R2 baseline. It measures grouped R→E MRR stratified by EC-4 group size (tail / mid / head) on R3 output embeddings. No training, model modification, or threshold calibration was performed.

## 2. Inputs

| File | Path |
|------|------|
| embeddings | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/embeddings_v3.npz` |
| metadata | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/metadata_v3.json` |
| metrics | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/metrics_v3.json` |
| eval script | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/code/demo/eval_ec4_buckets.py` |

## 3. Command

```bash
/public/home/acfbwjsi7s/miniconda3/envs/nis/bin/python eval_ec4_buckets.py \
    --output_dir /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15 \
    --report_path /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_ec4_bucket_eval.md \
    --chunk_size 1024
```

## 4. Bucket Definitions

| Bucket | Rule |
|--------|------|
| tail | EC-4 group size ≤ 4 |
| mid | 5 ≤ EC-4 group size ≤ 317 |
| head | EC-4 group size > 317 |

## 5. R3 Bucket Metrics

| Bucket | n groups | n rows | MRR | top-1 | top-5 | top-10 |
|--------|----------|--------|-----|-------|-------|--------|
| tail | 1397 | 2783 | 0.943734 | 0.820697 | 0.941789 | 0.961193 |
| mid | 1000 | 45030 | 0.909006 | 0.835199 | 0.921608 | 0.931623 |
| head | 127 | 80034 | 0.922084 | 0.856811 | 0.939638 | 0.950946 |
| **ALL** | **2524** | **127847** | **0.917949** | **0.848413** | **0.933334** | **0.944363** |

## 6. Overall Consistency Check

| Metric | Value |
|--------|-------|
| Computed overall valid EC-4 grouped MRR | **0.9179491188** |
| metrics_v3 EC-4-grouped MRR | **0.9184038175** |
| Relative error | 4.951e-04 |
| Tolerance | 0.01 |
| Status | **PASS** |

## 7. R2 vs R3 Bucket Comparison

| Bucket | Metric | R2 | R3 | Abs Δ | Rel Δ (%) |
|--------|--------|-----|-----|--------|-----------|
| tail | MRR | 0.904378 | 0.943734 | +0.039356 | +4.35 |
| tail | top-1 | 0.763205 | 0.820697 | +0.057492 | +7.53 |
| tail | top-5 | 0.915199 | 0.941789 | +0.026590 | +2.91 |
| tail | top-10 | 0.937837 | 0.961193 | +0.023356 | +2.49 |
| mid | MRR | 0.911926 | 0.909006 | −0.002920 | −0.32 |
| mid | top-1 | 0.828692 | 0.835199 | +0.006507 | +0.79 |
| mid | top-5 | 0.915901 | 0.921608 | +0.005707 | +0.62 |
| mid | top-10 | 0.936775 | 0.931623 | −0.005152 | −0.55 |
| head | MRR | 0.915733 | 0.922084 | +0.006351 | +0.69 |
| head | top-1 | 0.850214 | 0.856811 | +0.006597 | +0.78 |
| head | top-5 | 0.953095 | 0.939638 | −0.013457 | −1.41 |
| head | top-10 | 0.965240 | 0.950946 | −0.014294 | −1.48 |
| **ALL** | **MRR** | **0.914145** | **0.917949** | **+0.003804** | **+0.42** |
| ALL | top-1 | 0.840739 | 0.848413 | +0.007674 | +0.91 |
| ALL | top-5 | 0.939169 | 0.933334 | −0.005835 | −0.62 |
| ALL | top-10 | 0.954618 | 0.944363 | −0.010255 | −1.07 |

## 8. Runtime

| Field | Value |
|-------|-------|
| Host | login01 |
| Python | 3.9.23 |
| NumPy | 1.26.4 |
| chunk_size | 1024 |
| Total chunks | 143 |
| Computation time | 1121.8s (~18.7 min) |
| Start | 16:20:09 |
| End | 16:38:53 |

## 9. Output Files

| File | Path |
|------|------|
| JSON report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_ec4_bucket_eval.json` |
| Script-generated markdown | `.../r3_ec4_balanced_stage3skip_2026-06-15/r3_ec4_bucket_eval.md` |
| Stdout log | `.../r3_ec4_balanced_stage3skip_2026-06-15/r3_bucket_eval.log` |
| This report | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/docs/R3_EC4_BUCKET_EVAL_20260615.md` |

## 10. Declarations

| Item | Status |
|------|--------|
| train.py modified | **no** |
| retraining executed | **no** |
| Slurm submitted | **no** |
| GPU/DCU used | **no** |
| existing embeddings only | **yes** |
| ready for local bucket audit | **yes** |
