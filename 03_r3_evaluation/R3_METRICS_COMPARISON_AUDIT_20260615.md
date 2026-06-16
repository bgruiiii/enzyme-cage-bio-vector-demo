# R3 Metrics Comparison Audit

**Date:** 2026-06-15
**R2 Job:** 115204112 (2026-06-11)
**R3 Job:** 115402116 (2026-06-15)

---

## 1. Data Sources

| Item | Path |
|------|------|
| R2 metrics | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r2_esmc_hardneg1_stage1_25_2026-06-11/metrics_v3.json` |
| R3 metrics | `/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/metrics_v3.json` |
| R2 training history | `...r2_esmc_hardneg1_stage1_25_2026-06-11/training_history.json` |
| R3 training history | `...r3_ec4_balanced_stage3skip_2026-06-15/training_history.json` |
| R3 config | `...r3_ec4_balanced_stage3skip_2026-06-15/r3_config.txt` |

---

## 2. R2 Metrics (Complete)

### Row-Level Cross-Modal Retrieval

| Metric | R2 Value |
|--------|----------|
| R→E top-1 | 0.01762 |
| R→E top-5 | 0.06043 |
| R→E top-10 | 0.09357 |
| R→E top-20 | 0.14063 |
| R→E MRR | 0.06021 |
| E→M top-1 | 0.00438 |
| E→M top-5 | 0.02124 |
| E→M top-10 | 0.03959 |
| E→M top-20 | 0.07000 |
| E→M MRR | 0.61955 |
| S→M top-1 | 0.00569 |
| S→M top-5 | 0.02510 |
| S→M top-10 | 0.04419 |
| S→M top-20 | 0.07599 |
| S→M MRR | 0.58706 |

### Grouped R→E Evaluation

| Metric | R2 Value |
|--------|----------|
| UniProt top-1 | 0.03531 |
| UniProt top-5 | 0.06919 |
| UniProt top-10 | 0.09855 |
| UniProt MRR | 0.06071 |
| UniProt evaluated | 145,607 |
| UniProt excluded | 0 |
| EC-2 top-1 | 0.89099 |
| EC-2 top-5 | 0.93771 |
| EC-2 top-10 | 0.95535 |
| EC-2 MRR | 0.93065 |
| EC-2 evaluated | 130,635 |
| EC-2 excluded | 14,972 |
| EC-3 top-1 | 0.88905 |
| EC-3 top-5 | 0.93761 |
| EC-3 top-10 | 0.95526 |
| EC-3 MRR | 0.93035 |
| EC-3 evaluated | 130,635 |
| EC-3 excluded | 14,972 |
| EC-4 top-1 | 0.83889 |
| EC-4 top-5 | 0.93887 |
| EC-4 top-10 | 0.95454 |
| EC-4 MRR | 0.91321 |
| EC-4 evaluated | 127,847 |
| EC-4 excluded | 17,760 |

---

## 3. R3 Metrics (Complete)

### Row-Level Cross-Modal Retrieval

| Metric | R3 Value |
|--------|----------|
| R→E top-1 | 0.01586 |
| R→E top-5 | 0.05568 |
| R→E top-10 | 0.08763 |
| R→E top-20 | 0.13401 |
| R→E MRR | 0.05465 |
| E→M top-1 | 0.00571 |
| E→M top-5 | 0.02244 |
| E→M top-10 | 0.03902 |
| E→M top-20 | 0.06726 |
| E→M MRR | 0.61567 |
| S→M top-1 | 0.00429 |
| S→M top-5 | 0.01937 |
| S→M top-10 | 0.03529 |
| S→M top-20 | 0.06284 |
| S→M MRR | 0.60050 |

### Grouped R→E Evaluation

| Metric | R3 Value |
|--------|----------|
| UniProt top-1 | 0.02913 |
| UniProt top-5 | 0.06332 |
| UniProt top-10 | 0.09240 |
| UniProt MRR | 0.05512 |
| UniProt evaluated | 145,607 |
| UniProt excluded | 0 |
| EC-2 top-1 | 0.90201 |
| EC-2 top-5 | 0.93715 |
| EC-2 top-10 | 0.96264 |
| EC-2 MRR | 0.93800 |
| EC-2 evaluated | 130,635 |
| EC-2 excluded | 14,972 |
| EC-3 top-1 | 0.90003 |
| EC-3 top-5 | 0.93706 |
| EC-3 top-10 | 0.96119 |
| EC-3 MRR | 0.93770 |
| EC-3 evaluated | 130,635 |
| EC-3 excluded | 14,972 |
| EC-4 top-1 | 0.85397 |
| EC-4 top-5 | 0.93198 |
| EC-4 top-10 | 0.94440 |
| EC-4 MRR | 0.91840 |
| EC-4 evaluated | 127,847 |
| EC-4 excluded | 17,760 |

---

## 4. R3 − R2 Delta Table

### Row-Level Cross-Modal Retrieval

| Metric | R2 | R3 | Abs Δ | Rel Δ (%) |
|--------|-----|-----|--------|-----------|
| R→E top-1 | 0.01762 | 0.01586 | −0.00176 | −9.98 |
| R→E top-5 | 0.06043 | 0.05568 | −0.00475 | −7.85 |
| R→E top-10 | 0.09357 | 0.08763 | −0.00594 | −6.35 |
| R→E top-20 | 0.14063 | 0.13401 | −0.00661 | −4.70 |
| R→E MRR | 0.06021 | 0.05465 | −0.00556 | −9.23 |
| E→M top-1 | 0.00438 | 0.00571 | +0.00133 | +30.28 |
| E→M top-5 | 0.02124 | 0.02244 | +0.00120 | +5.63 |
| E→M top-10 | 0.03959 | 0.03902 | −0.00057 | −1.44 |
| E→M top-20 | 0.07000 | 0.06726 | −0.00273 | −3.91 |
| E→M MRR | 0.61955 | 0.61567 | −0.00388 | −0.63 |
| S→M top-1 | 0.00569 | 0.00429 | −0.00141 | −24.73 |
| S→M top-5 | 0.02510 | 0.01937 | −0.00573 | −22.85 |
| S→M top-10 | 0.04419 | 0.03529 | −0.00890 | −20.14 |
| S→M top-20 | 0.07599 | 0.06284 | −0.01314 | −17.30 |
| S→M MRR | 0.58706 | 0.60050 | +0.01344 | +2.29 |

### Grouped R→E Evaluation

| Metric | R2 | R3 | Abs Δ | Rel Δ (%) |
|--------|-----|-----|--------|-----------|
| UniProt top-1 | 0.03531 | 0.02913 | −0.00618 | −17.51 |
| UniProt top-5 | 0.06919 | 0.06332 | −0.00587 | −8.48 |
| UniProt top-10 | 0.09855 | 0.09240 | −0.00615 | −6.24 |
| UniProt MRR | 0.06071 | 0.05512 | −0.00558 | −9.20 |
| EC-2 top-1 | 0.89099 | 0.90201 | +0.01102 | +1.24 |
| EC-2 top-5 | 0.93771 | 0.93715 | −0.00056 | −0.06 |
| EC-2 top-10 | 0.95535 | 0.96264 | +0.00730 | +0.76 |
| EC-2 MRR | 0.93065 | 0.93800 | +0.00736 | +0.79 |
| EC-3 top-1 | 0.88905 | 0.90003 | +0.01098 | +1.23 |
| EC-3 top-5 | 0.93761 | 0.93706 | −0.00055 | −0.06 |
| EC-3 top-10 | 0.95526 | 0.96119 | +0.00593 | +0.62 |
| EC-3 MRR | 0.93035 | 0.93770 | +0.00735 | +0.79 |
| EC-4 top-1 | 0.83889 | 0.85397 | +0.01507 | +1.80 |
| EC-4 top-5 | 0.93887 | 0.93198 | −0.00689 | −0.73 |
| EC-4 top-10 | 0.95454 | 0.94440 | −0.01014 | −1.06 |
| EC-4 MRR | 0.91321 | 0.91840 | +0.00519 | +0.57 |

---

## 5. Training History Structure Check

| Field | R2 | R3 |
|-------|-----|-----|
| Total epochs | 51 | 38 |
| loss array length | 51 | 38 |
| temp array length | 51 | 38 |
| stage array length | 51 | 38 |
| Stage 0 epochs | 8 (idx 0–7) | 5 (idx 0–4) |
| Stage 1 epochs | 25 (idx 8–32) | 25 (idx 5–29) |
| Stage 2 epochs | 8 (idx 33–40) | 8 (idx 30–37) |
| Stage 3 epochs | 10 (idx 41–50) | 0 (none) |
| Final loss | 44.677 | 42.812 |
| Initial loss | 2.816 | 2.816 |
| Final τ | 0.050 | 0.050 |
| Initial τ | 0.500 | 0.500 |

---

## 6. R3 Config

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

## 7. Declarations

| Item | Status |
|------|--------|
| train.py modified | **no** |
| retraining executed | **no** |
| only existing metrics read | **yes** |
| R2/R3 comparison executed | **yes** |
| ready for local metrics audit | **yes** |
