# Bio Vector R3 Result Summary

Date: 2026-06-15

This summary consolidates the completed R3 training and evaluation artifacts. It uses only existing R2/R3 outputs and the audited post-run reports listed below. No additional training or metric recomputation is introduced in this file.

## 1. HPC Artifacts

| Item | Value |
|---|---|
| R3 training job | `115402116` |
| R3 training state | `COMPLETED`, exit code `0:0` |
| R3 training elapsed | `03:23:28` |
| R3 training node | `f13r4n19` |
| R3 output directory | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15` |
| Stage-wise eval job | `115418482` |
| Stage-wise eval state | `COMPLETED`, exit code `0:0` |
| Stage-wise eval elapsed | `04:40:29` |
| Stage-wise eval node | `f13r4n19` |

Audited source documents:

| Evidence | Local path |
|---|---|
| Training completion | `custom/docs/bio_vector/R3_TRAIN_COMPLETION_AUDIT_20260615.md` |
| Metrics comparison | `custom/docs/bio_vector/R3_METRICS_COMPARISON_AUDIT_20260615.md` |
| EC-4 bucket evaluation | `custom/docs/bio_vector/R3_EC4_BUCKET_EVAL_20260615.md` |
| Stage-wise checkpoint evaluation | `custom/docs/bio_vector/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md` |
| R2 bucket baseline | `custom/docs/bio_vector/R2_EC4_BUCKET_BASELINE.md` |

## 2. Core Artifacts

R3 output directory file set:

| Artifact | Status / size |
|---|---:|
| `model_v3.pt` | present, 24M |
| `model_v3_stage0.pt` | present, 19M |
| `model_v3_stage1.pt` | present, 19M |
| `model_v3_stage2.pt` | present, 19M |
| `model_v3_stage3.pt` | present, 19M |
| `embeddings_v3.npz` | present, 569M |
| `metrics_v3.json` | present, 1.7K |
| `metadata_v3.json` | present, 22M |
| `training_history.json` | present, 2.1K |
| `r3_config.txt` | present, 258B |
| `reaction_nn_index.npz` | present, 143M |
| `enzyme_nn_index.npz` | present, 143M |
| `substrate_nn_index.npz` | present, 143M |
| `microbe_nn_index.npz` | present, 143M |
| `enzyme2microbe_index.json` | present, 4.3M |

Embedding structure:

| Array | Shape | Dtype |
|---|---:|---|
| `reaction` | `(145607, 256)` | `float32` |
| `enzyme` | `(145607, 256)` | `float32` |
| `substrate` | `(145607, 256)` | `float32` |
| `microbe` | `(145607, 256)` | `float32` |

R3 config:

```text
epochs_stage0=5
epochs_stage1=25
epochs_stage2=8
epochs_stage3=0 (stage3 skip, alias from stage2)
hard_neg_weight=1.0
ec4_weighted_sampler=stage1/stage2
train.py md5: 4d9378e15e42723e3f1ebc1dcf629cfb
```

Stage 3 alias check:

| File | MD5 |
|---|---|
| `model_v3_stage2.pt` | `c014e346a2f4f5c5b15b9575d73e2c45` |
| `model_v3_stage3.pt` | `c014e346a2f4f5c5b15b9575d73e2c45` |

`model_v3_stage3.pt` is a byte-identical alias/reference copy of `model_v3_stage2.pt`, as intended for `epochs_stage3=0`.

## 3. R3 Metrics vs R2

### 3.1 Row-Level Cross-Modal Retrieval

| Metric | R2 | R3 | Abs delta | Rel delta (%) |
|---|---:|---:|---:|---:|
| R->E top-1 | 0.01762 | 0.01586 | -0.00176 | -9.98 |
| R->E top-5 | 0.06043 | 0.05568 | -0.00475 | -7.85 |
| R->E top-10 | 0.09357 | 0.08763 | -0.00594 | -6.35 |
| R->E top-20 | 0.14063 | 0.13401 | -0.00661 | -4.70 |
| R->E MRR | 0.06021 | 0.05465 | -0.00556 | -9.23 |
| E->M top-1 | 0.00438 | 0.00571 | +0.00133 | +30.28 |
| E->M top-5 | 0.02124 | 0.02244 | +0.00120 | +5.63 |
| E->M top-10 | 0.03959 | 0.03902 | -0.00057 | -1.44 |
| E->M top-20 | 0.07000 | 0.06726 | -0.00273 | -3.91 |
| E->M MRR | 0.61955 | 0.61567 | -0.00388 | -0.63 |
| S->M top-1 | 0.00569 | 0.00429 | -0.00141 | -24.73 |
| S->M top-5 | 0.02510 | 0.01937 | -0.00573 | -22.85 |
| S->M top-10 | 0.04419 | 0.03529 | -0.00890 | -20.14 |
| S->M top-20 | 0.07599 | 0.06284 | -0.01314 | -17.30 |
| S->M MRR | 0.58706 | 0.60050 | +0.01344 | +2.29 |

### 3.2 Grouped R->E Evaluation

| Metric | R2 | R3 | Abs delta | Rel delta (%) |
|---|---:|---:|---:|---:|
| UniProt top-1 | 0.03531 | 0.02913 | -0.00618 | -17.51 |
| UniProt top-5 | 0.06919 | 0.06332 | -0.00587 | -8.48 |
| UniProt top-10 | 0.09855 | 0.09240 | -0.00615 | -6.24 |
| UniProt MRR | 0.06071 | 0.05512 | -0.00558 | -9.20 |
| EC-2 top-1 | 0.89099 | 0.90201 | +0.01102 | +1.24 |
| EC-2 top-5 | 0.93771 | 0.93715 | -0.00056 | -0.06 |
| EC-2 top-10 | 0.95535 | 0.96264 | +0.00730 | +0.76 |
| EC-2 MRR | 0.93065 | 0.93800 | +0.00736 | +0.79 |
| EC-3 top-1 | 0.88905 | 0.90003 | +0.01098 | +1.23 |
| EC-3 top-5 | 0.93761 | 0.93706 | -0.00055 | -0.06 |
| EC-3 top-10 | 0.95526 | 0.96119 | +0.00593 | +0.62 |
| EC-3 MRR | 0.93035 | 0.93770 | +0.00735 | +0.79 |
| EC-4 top-1 | 0.83889 | 0.85397 | +0.01507 | +1.80 |
| EC-4 top-5 | 0.93887 | 0.93198 | -0.00689 | -0.73 |
| EC-4 top-10 | 0.95454 | 0.94440 | -0.01014 | -1.06 |
| EC-4 MRR | 0.91321 | 0.91840 | +0.00519 | +0.57 |

### 3.3 EC-4 Bucket Evaluation

Bucket rules use the same script and definitions as the R2 baseline:

| Bucket | Rule |
|---|---|
| tail | EC-4 group size <= 4 |
| mid | 5 <= EC-4 group size <= 317 |
| head | EC-4 group size > 317 |

R3 bucket metrics:

| Bucket | n groups | n rows | MRR | top-1 | top-5 | top-10 |
|---|---:|---:|---:|---:|---:|---:|
| tail | 1397 | 2783 | 0.943734 | 0.820697 | 0.941789 | 0.961193 |
| mid | 1000 | 45030 | 0.909006 | 0.835199 | 0.921608 | 0.931623 |
| head | 127 | 80034 | 0.922084 | 0.856811 | 0.939638 | 0.950946 |
| ALL | 2524 | 127847 | 0.917949 | 0.848413 | 0.933334 | 0.944363 |

R2 vs R3 bucket comparison:

| Bucket | Metric | R2 | R3 | Abs delta | Rel delta (%) |
|---|---|---:|---:|---:|---:|
| tail | MRR | 0.904378 | 0.943734 | +0.039356 | +4.35 |
| tail | top-1 | 0.763205 | 0.820697 | +0.057492 | +7.53 |
| tail | top-5 | 0.915199 | 0.941789 | +0.026590 | +2.91 |
| tail | top-10 | 0.937837 | 0.961193 | +0.023356 | +2.49 |
| mid | MRR | 0.911926 | 0.909006 | -0.002920 | -0.32 |
| mid | top-1 | 0.828692 | 0.835199 | +0.006507 | +0.79 |
| mid | top-5 | 0.915901 | 0.921608 | +0.005707 | +0.62 |
| mid | top-10 | 0.936775 | 0.931623 | -0.005152 | -0.55 |
| head | MRR | 0.915733 | 0.922084 | +0.006351 | +0.69 |
| head | top-1 | 0.850214 | 0.856811 | +0.006597 | +0.78 |
| head | top-5 | 0.953095 | 0.939638 | -0.013457 | -1.41 |
| head | top-10 | 0.965240 | 0.950946 | -0.014294 | -1.48 |
| ALL | MRR | 0.914145 | 0.917949 | +0.003804 | +0.42 |
| ALL | top-1 | 0.840739 | 0.848413 | +0.007674 | +0.91 |
| ALL | top-5 | 0.939169 | 0.933334 | -0.005835 | -0.62 |
| ALL | top-10 | 0.954618 | 0.944363 | -0.010255 | -1.07 |

R3 bucket ALL MRR consistency check:

| Item | Value |
|---|---:|
| Computed ALL MRR | 0.9179491188 |
| `metrics_v3.json` EC-4 grouped MRR | 0.9184038175 |
| Relative error | 4.951e-04 |
| Tolerance | 0.01 |
| Status | PASS |

## 4. Teacher Criteria Table

This table follows the quantitative criteria in the teacher-provided R3 plan. Calibration, OOD, and latency are not added to R3 acceptance.

| Criterion | R2 baseline | R3 value | Teacher target | PASS/FAIL |
|---|---:|---:|---:|---|
| EC-4-grouped R->E MRR | 0.9132 | 0.9184 | >= 0.9132 | PASS |
| E->M MRR | 0.6195 | 0.6157 | >= 0.6100 | PASS |
| EC-2-grouped R->E MRR | 0.9306 | 0.9380 | >= 0.9200 | PASS |
| EC-4 tail bucket MRR | 0.904378 | 0.943734 | >= 0.949597 | FAIL: +4.35% vs +5% target |
| EC-4 head bucket MRR | 0.915733 | 0.922084 | >= 0.888261 | PASS |
| row-level R->E MRR | 0.0602 | 0.0547 | reference only | Reference |
| Stage training time | 03:24:55 | 03:23:28 | < 03:00:00 | FAIL: time is similar to R2 |

Primary EC-4 grouped R->E MRR improved from 0.91321 to 0.91840. The long-tail bucket improved from 0.904378 to 0.943734, but the relative change is +4.35% while the teacher target is +5%. The head bucket MRR is above the R2-minus-3% guardrail.

## 5. Stage-Wise Checkpoint MRR Evolution

The R3 stage-wise evaluation used `postmortem_eval_stage_checkpoints.py` on all four saved checkpoint files. Because `epochs_stage3=0`, `model_v3_stage3.pt` is an alias/reference copy of `model_v3_stage2.pt`; the full stage-wise scope was still evaluated.

| Stage | row R->E MRR | UniProt grouped R->E MRR | EC-4 grouped R->E MRR | E->M MRR | elapsed_seconds |
|---|---:|---:|---:|---:|---:|
| stage0 | 0.000095 | 0.000095 | 0.008089 | 0.000767 | 2606.67 |
| stage1 | 0.054643 | 0.055008 | 0.925248 | 0.616432 | 2258.33 |
| stage2 | 0.054745 | 0.055119 | 0.924295 | 0.618950 | 2241.47 |
| stage3 | 0.054745 | 0.055119 | 0.924295 | 0.618950 | 2248.86 |

Stage transition deltas:

| Transition | row R->E MRR | UniProt grouped R->E MRR | EC-4 grouped R->E MRR | E->M MRR |
|---|---:|---:|---:|---:|
| stage1 - stage0 | +0.054548 | +0.054913 | +0.917159 | +0.615665 |
| stage2 - stage1 | +0.000102 | +0.000111 | -0.000953 | +0.002518 |
| stage3 - stage2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

Stage-wise note:

- Stage1 accounts for the main jump in EC-4 grouped R->E MRR.
- Stage2 changes the monitored MRRs only slightly relative to stage1.
- Stage3 equals stage2 because it is a checkpoint alias/reference under `epochs_stage3=0`.

## 6. Training Time Comparison

| Run | Job ID | Epochs | Stage config | Elapsed |
|---|---:|---:|---|---:|
| R2 | `115204112` | 51 | 8 / 25 / 8 / 10 | 03:24:55 |
| R3 | `115402116` | 38 | 5 / 25 / 8 / 0 | 03:23:28 |

Time delta:

| Metric | Value |
|---|---:|
| Absolute time delta | -00:01:27 |
| Relative time delta | -0.71% |
| Teacher target | < 03:00:00 |

R3 reduced total epochs from 51 to 38 and skipped independent stage3 training, but the recorded end-to-end training elapsed time remained close to R2. The training log confirms that stage3 was skipped and `model_v3_stage3.pt` was copied from the stage2 checkpoint.

## 7. Provenance and Declarations

| Item | Status |
|---|---|
| `train.py` modified by this summary | no |
| Retraining executed by this summary | no |
| Existing R2/R3 outputs only | yes |
| R3 training completed | yes |
| R3 metrics compared to R2 | yes |
| R3 bucket table included | yes |
| Stage-wise checkpoint table included | yes |
| R4 plan details included | no |

Next required deliverable from the teacher checklist is `R4_DECISION_INPUT.md` as a decision input only, not an R4 training plan.
