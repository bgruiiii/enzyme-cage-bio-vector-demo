# R3 Stage-Wise Checkpoint Evaluation — Completion Audit Report

**Date:** 2026-06-15  
**Job ID:** 115418482  
**Report Type:** Post-run completion audit (stage-wise checkpoint evaluation only)

---

## 1. Job 状态

| Field     | Value          |
|-----------|----------------|
| Job ID    | 115418482      |
| JobName   | r3_stage_eval  |
| Partition | kshdnormal04   |
| State     | **COMPLETED**  |
| ExitCode  | **0:0**        |
| Elapsed   | 04:40:29       |
| MaxRSS    | 25,293,412 K (~24.1 GB) |
| NodeList  | f13r4n19       |

---

## 2. 输入与输出路径

### Stage Checkpoint Paths

| Stage   | Checkpoint Path                                                                                         | MD5                              | Size    |
|---------|---------------------------------------------------------------------------------------------------------|----------------------------------|---------|
| stage0  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/model_v3_stage0.pt` | `e64f4081f0c87344af1030977c6e5541` | 19.7 MB |
| stage1  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/model_v3_stage1.pt` | `2d7e671d36b7aaf7ead25de8f6b1a659` | 19.7 MB |
| stage2  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/model_v3_stage2.pt` | `c014e346a2f4f5c5b15b9575d73e2c45` | 19.7 MB |
| stage3  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/model_v3_stage3.pt` | `c014e346a2f4f5c5b15b9575d73e2c45` | 19.7 MB |

### Other Paths

| Item                        | Path                                                                                                      |
|-----------------------------|-----------------------------------------------------------------------------------------------------------|
| data_dir                    | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/data/reaction_enzyme_microbe_training_clean_2026-06-01_LOCAL` |
| output_dir                  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15`   |
| postmortem_stage_eval.json  | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/postmortem_stage_eval.json` (9060 bytes) |
| stdout                      | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_stage_eval_115418482.out` |
| stderr                      | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/r3_stage_eval_115418482.err` |

---

## 3. Stage-Wise MRR 表

数据来源: `postmortem_stage_eval.json`

| Stage  | row R→E MRR | UniProt-grouped R→E MRR | EC-4-grouped R→E MRR | E→M MRR  | elapsed_seconds |
|--------|-------------|-------------------------|----------------------|----------|-----------------|
| stage0 | 0.000095    | 0.000095                | 0.008089             | 0.000767 | 2606.67         |
| stage1 | 0.054643    | 0.055008                | 0.925248             | 0.616432 | 2258.33         |
| stage2 | 0.054745    | 0.055119                | 0.924295             | 0.618950 | 2241.47         |
| stage3 | 0.054745    | 0.055119                | 0.924295             | 0.618950 | 2248.86         |

> 全部 4 个 stage checkpoint 均已完成 evaluation，结果完整无缺失。

---

## 4. Stage Transition Delta 表

### Stage 1 − Stage 0

| Metric                    | Delta        |
|---------------------------|--------------|
| row R→E MRR              | +0.054548    |
| UniProt-grouped R→E MRR  | +0.054913    |
| EC-4-grouped R→E MRR     | +0.917159    |
| E→M MRR                  | +0.615665    |

### Stage 2 − Stage 1

| Metric                    | Delta        |
|---------------------------|--------------|
| row R→E MRR              | +0.000102    |
| UniProt-grouped R→E MRR  | +0.000111    |
| EC-4-grouped R→E MRR     | −0.000953    |
| E→M MRR                  | +0.002518    |

### Stage 3 − Stage 2

| Metric                    | Delta        |
|---------------------------|--------------|
| row R→E MRR              | 0.000000     |
| UniProt-grouped R→E MRR  | 0.000000     |
| EC-4-grouped R→E MRR     | 0.000000     |
| E→M MRR                  | 0.000000     |

> Stage 3 与 Stage 2 的 MRR 值完全一致（所有 delta = 0），与 stage3.pt 作为 stage2.pt alias 的设计一致。

---

## 5. Stage 3 Alias Note

- **MD5 一致性验证:**
  - `model_v3_stage2.pt`: `c014e346a2f4f5c5b15b9575d73e2c45`
  - `model_v3_stage3.pt`: `c014e346a2f4f5c5b15b9575d73e2c45`
  - **结论: stage3.pt 与 stage2.pt 二进制完全相同 (MD5 match)。**

- **Stage 3 定位:**
  - stage3 是 stage2 checkpoint 的 alias / reference copy，不是独立训练阶段。
  - 本次按老师要求完成了 stage0 / stage1 / stage2 / stage3 全部 checkpoint 的 evaluation。
  - stage3 evaluation 结果与 stage2 完全一致，验证了 alias 关系的正确性。

- **Consistency Check (stdout 摘录):**

```
row_RE_MRR: actual=0.054745, expected=0.054650, rel_err=0.0017 [PASS]
UniProt_grouped_RE_MRR: actual=0.055119, expected=0.055123, rel_err=0.0001 [PASS]
EC4_grouped_RE_MRR: actual=0.924295, expected=0.918404, rel_err=0.0064 [PASS]
EM_MRR: actual=0.618950, expected=0.615667, rel_err=0.0053 [PASS]
Consistency check: ALL PASS
```

---

## 6. Stdout / Stderr Tail 摘录

### Stderr 分析

stderr 全文 **仅包含** `DEPRECATION WARNING: please use MorganGenerator` 警告（来自 rdkit Morgan fingerprint 模块），以及可能的 torch deprecation warning。

**未发现以下任何关键词:**

- `error` — 无
- `traceback` — 无
- `oom` — 无
- `killed` — 无
- `stopped` — 无

> stderr 内容全部为第三方库的 deprecation 级别 warning，不影响 evaluation 正确性。

### Stdout 关键摘录

```
=== R3 Stage-Wise Checkpoint Evaluation ===
hostname: f13r4n19
date: Mon Jun 15 17:00:42 CST 2026
  Microbe records from CSV tables: 145607
  ESM-C available UIDs: 107731
  Total samples: 145607
  Dims: reaction=2048, enzyme=1152, substrate=2048, microbe=28
  Data loaded in 7389.6s
=== Evaluating 4 checkpoint(s) ===
  Stage 0 evaluated in 2606.7s
  Stage 1 evaluated in 2258.3s
  Stage 2 evaluated in 2241.5s
  Stage 3 evaluated in 2248.9s
Consistency check: ALL PASS
=== R3 Stage Evaluation Complete ===
date: Mon Jun 15 21:41:10 CST 2026
```

---

## 7. 声明

| Item                                     | Value   |
|------------------------------------------|---------|
| train.py modified                        | **no**  |
| run_r3_training.sh modified              | **no**  |
| retraining executed                      | **no**  |
| only checkpoint evaluation executed      | **yes** |
| Slurm submitted                          | **yes** |
| GPU/DCU used                             | **yes, evaluation only** |
| teacher-requested stage-wise scope preserved | **yes** |
| ready for local stagewise completion audit | **yes** |

---

*Report generated: 2026-06-15*
