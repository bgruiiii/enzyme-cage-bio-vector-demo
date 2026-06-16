# R3 Training Completion Audit

**Date:** 2026-06-15
**Job ID:** 115402116
**Status:** ✅ COMPLETED (Exit Code 0:0)

---

## 1. Job Status

```
JobID                                   JobName Partition           State ExitCode    Elapsed     MaxRSS        NodeList
---------------- ------------------------------ -------------- ---------- -------- ---------- ---------- ---------------
115402116                       r3_ec4_balanced kshdnormal04    COMPLETED      0:0   03:23:28                   f13r4n19
115402116.batch                           batch                 COMPLETED      0:0   03:23:28  27469288K        f13r4n19
115402116.extern                         extern                 COMPLETED      0:0   03:23:28      3360K        f13r4n19
```

| Field | Value |
|-------|-------|
| State | COMPLETED |
| Exit Code | 0:0 |
| Elapsed | 03:23:28 |
| MaxRSS | 27,469,288K (~26.2 GB) |
| Node | f13r4n19 |
| Partition | kshdnormal04 |

---

## 2. Output Directory File Listing

```
total 1.3G
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 569M Jun 15 14:59 embeddings_v3.npz
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 4.3M Jun 15 14:59 enzyme2microbe_index.json
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 143M Jun 15 14:59 enzyme_nn_index.npz
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  22M Jun 15 14:59 metadata_v3.json
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 1.7K Jun 15 14:59 metrics_v3.json
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 143M Jun 15 14:59 microbe_nn_index.npz
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  24M Jun 15 14:22 model_v3.pt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  19M Jun 15 14:16 model_v3_stage0.pt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  19M Jun 15 14:20 model_v3_stage1.pt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  19M Jun 15 14:22 model_v3_stage2.pt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  19M Jun 15 14:22 model_v3_stage3.pt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s  258 Jun 15 11:38 r3_config.txt
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 8.2M Jun 15 14:16 r3_train_115402116.err
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 6.1K Jun 15 15:00 r3_train_115402116.out
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 143M Jun 15 14:59 reaction_nn_index.npz
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 143M Jun 15 14:59 substrate_nn_index.npz
-rw-rw-r-- 1 acfbwjsi7s acfbwjsi7s 2.1K Jun 15 14:22 training_history.json
```

**Total: 17 files, 1.3 GB**

---

## 3. Required Artifacts Check

| File | Status | Size |
|------|--------|------|
| `model_v3.pt` | ✅ OK | 24M |
| `model_v3_stage0.pt` | ✅ OK | 19M |
| `model_v3_stage1.pt` | ✅ OK | 19M |
| `model_v3_stage2.pt` | ✅ OK | 19M |
| `model_v3_stage3.pt` | ✅ OK | 19M |
| `embeddings_v3.npz` | ✅ OK | 569M |
| `metrics_v3.json` | ✅ OK | 1.7K |
| `metadata_v3.json` | ✅ OK | 22M |
| `training_history.json` | ✅ OK | 2.1K |
| `r3_config.txt` | ✅ OK | 258B |
| `r3_train_115402116.out` | ✅ OK | 6.1K |
| `r3_train_115402116.err` | ✅ OK | 8.2M |

**All 12 required artifacts: PRESENT ✅**

---

## 4. Stdout Tail

```
step: config recorded
step: starting R3 training
  epochs_stage0=5 (R2 was 8)
  epochs_stage1=25 (unchanged)
  epochs_stage2=8 (unchanged)
  epochs_stage3=0 (R2 was 10, stage3 skip)
  hard_neg_weight=1.0 (unchanged)
  EC-4 weighted sampler for stage1/stage2
  Total epochs: 5+25+8+0 = 38
Device: cuda
Mode: enzyme_cage_300
Unified dim: 256
Temperature: 0.5 → 0.05 (cosine annealing)
VICReg: var_w=10.0, cov_w=1.0
Three-way weights: w_re=1.0, w_em=0.7, w_sm=0.5
  ...
  Total samples: 145607
  Dims: reaction=2048, enzyme=1152, substrate=2048, microbe=28
  EC-4 weighted sampler built for 145607 train samples
  Model parameters: 4,831,752

Starting 4-stage training (38 total epochs)
  Stage 0 (pretrain):         5 epochs
  Stage 1 (pairwise):         25 epochs
  Stage 2 (triplet+anchor):   8 epochs
  Stage 3 (self-bootstrap):   0 epochs

  [Stage 0] epoch   1/38  loss=2.8158  τ=0.5000
  Stage 0 checkpoint saved → model_v3_stage0.pt
  Stage 1: EC-4 weighted sampler activated
  [Stage 1] epoch  10/38  loss=39.0216  τ=0.4374
  [Stage 1] epoch  20/38  loss=36.9019  τ=0.2655
  [Stage 1] epoch  30/38  loss=32.4110  τ=0.0999
  Stage 1 checkpoint saved → model_v3_stage1.pt
  Stage 2 checkpoint saved → model_v3_stage2.pt
  Stage 3 skipped (epochs_stage3=0); model_v3_stage3.pt is alias of stage2 checkpoint

  Chunked R→E retrieval: 145607 queries
  Chunked E→M retrieval: 145607 queries
  Chunked S→M retrieval: 145607 queries

  EC-4-grouped R→E:  evaluated=127847  excluded_unknown=17760
    top-1=0.853966  top-5=0.931981  top-10=0.944402  MRR=0.918404

  FAISS SWIG incompatible with numpy 1.26.4, skipping native index (×4)
  Numpy NN fallback indices saved: 4 (*_nn_index.npz)
  WARNING: visualize_four_modal could not complete: object __array__ method not producing an array
  PNG visualization skipped; model/embeddings/metrics/index outputs are unaffected.

step: training complete
  OK: model_v3.pt
  OK: model_v3_stage0.pt
  OK: model_v3_stage1.pt
  OK: model_v3_stage2.pt
  OK: model_v3_stage3.pt
  OK: embeddings_v3.npz
  OK: metrics_v3.json
  OK: metadata_v3.json
  OK: training_history.json
step: verification complete
=== R3 Job finished ===
```

---

## 5. Stderr Tail

stderr 仅包含非致命信息：
- **MorganGenerator deprecation warnings** (rdkit): 大量重复的 `[DEPRECATION WARNING: please use MorganGenerator]`，不影响功能
- **torch.tensor UserWarning**: `train.py:191: To copy construct from a tensor, it is recommended to use sourceTensor.clone().detach()` — 已知非致命警告

**无 ERROR、无 crash、无 OOM。**

---

## 6. JSON/NPZ Structure Check

### metrics_v3.json (1,717 bytes, dict)
```
keys: E→M_MRR, E→M_top-1, E→M_top-10, E→M_top-20, E→M_top-5,
      R→E_MRR, R→E_top-1, R→E_top-10, R→E_top-20, R→E_top-5,
      S→M_MRR, S→M_top-1, S→M_top-10, S→M_top-20, S→M_top-5,
      grouped_re
```

### metadata_v3.json (22,711,862 bytes, list)
```
list_len: 145607
first_keys: assembly_accession, ec_number, example_id, uniprot_id
```

### training_history.json (2,104 bytes, dict)
```
keys: loss, stage, temp
```
38 epochs recorded (matching total_epochs = 38).

### embeddings_v3.npz (596,407,282 bytes)
```
npz_keys: enzyme, microbe, reaction, substrate
enzyme    (145607, 256) float32
microbe   (145607, 256) float32
reaction  (145607, 256) float32
substrate (145607, 256) float32
```

All 4 modalities present, shape matches (145607 samples × 256 dim), dtype float32.

---

## 7. Stage 3 Alias Check

```
=== ls -lh ===
-rw-rw-r-- model_v3_stage2.pt  19M Jun 15 14:22
-rw-rw-r-- model_v3_stage3.pt  19M Jun 15 14:22

=== md5sum ===
c014e346a2f4f5c5b15b9575d73e2c45  model_v3_stage2.pt
c014e346a2f4f5c5b15b9575d73e2c45  model_v3_stage3.pt
```

**MD5 完全一致 ✅** — `model_v3_stage3.pt` 是 `model_v3_stage2.pt` 的正确副本（`shutil.copy2` 按预期工作）。

---

## 8. R3 Config Confirmation

```
epochs_stage0=5
epochs_stage1=25
epochs_stage2=8
epochs_stage3=0 (stage3 skip, alias from stage2)
hard_neg_weight=1.0
ec4_weighted_sampler=stage1/stage2
R3 plan: docs/R3_TRAIN_PATCH_CORRECTIVE_AUDIT_20260615.md
train.py md5: 4d9378e15e42723e3f1ebc1dcf629cfb
```

---

## 9. Declarations

| Item | Status |
|------|--------|
| train.py modified after submission | **no** |
| run script modified after submission | **no** |
| Slurm job completed | **yes** |
| Exit code | **0:0** |
| Result analysis executed | **no** |
| R2/R3 comparison executed | **no** |
| Ready for local completion audit | **yes** |

---

## 10. Key Observations (non-analysis)

| Observation | Detail |
|-------------|--------|
| Stage 3 skip | ✅ 按预期工作，stage3.pt = stage2.pt |
| EC-4 weighted sampler | ✅ Stage 1 入口打印 "EC-4 weighted sampler activated" |
| Total epochs | ✅ 38 (5+25+8+0) |
| FAISS | SWIG 与 numpy 1.26.4 不兼容，使用 numpy NN fallback（4 个模态） |
| visualize_four_modal | try/except 捕获异常，warning 文案 "could not complete"，未导致 job 退出 |
| stderr | 仅 MorganGenerator deprecation + torch.tensor UserWarning，无 ERROR |
| Embeddings shape | 4 × (145607, 256) float32 — 符合预期 |
| Metadata count | 145,607 rows — 与 R2 一致 |
