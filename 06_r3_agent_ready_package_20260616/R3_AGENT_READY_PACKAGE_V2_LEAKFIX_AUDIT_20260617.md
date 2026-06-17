# R3 Agent-Ready Package v2 Leak-Fix Audit

**Timestamp**: 2026-06-17  
**Package**: `enzyme-cage-bio-vector-demo/06_r3_agent_ready_package_20260616`  
**Scope**: local package audit after Leave-EC4-Out v2 leak-fix validation  

## 1. Purpose

This document records the final local audit and manifest update for the R3
agent-ready package after the Leave-EC4-Out v2 leak-fix evaluation.

The audit distinguishes:

- v1 Leave-EC4-Out: retained as leaked row-level self-alignment audit evidence.
- v2 Leave-EC4-Out: final cross-class EC-family transfer validation under
  teacher tolerance.

This audit does not claim remote GitHub verification or HPC output-path
verification. Those require a separate remote/HPC check.

## 2. Package Manifest

| File | Size | Role |
|---|---:|---|
| `README.md` | 1774 bytes | Package index and final status |
| `eval_leave_ec4_out.py` | 32375 bytes | Final v2 zero-GPU leak-fix evaluation script |
| `R3_LEAVE_EC4_OUT_20260616_171432.md` | 3569 bytes | Legacy v1 path; superseded/leaked audit evidence only |
| `R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md` | 3569 bytes | Explicit v1 leaked audit report |
| `R3_LEAVE_EC4_OUT_v2_20260617_001330.md` | 4916 bytes | Final v2 Leave-EC4-Out validation report |
| `r3_leave_ec4_out.json` | 328391 bytes | v1 raw audit data; retained for traceability only |
| `r3_leave_ec4_out_v2.json` | 334753 bytes | Final v2 raw audit data |
| `R3_ACCEPTANCE_NOTE_20260616_173549.md` | 4123 bytes | R3 acceptance note updated for v2 |
| `R3_MODEL_FREEZE_20260616_174232.md` | 4083 bytes | Freeze evidence; provenance wording updated for v2 |
| `R3_AGENT_INTEGRATION_PREREQUISITES.md` | 4922 bytes | Agent policy prerequisites updated for v2 |

All listed files are present and non-empty in the local package copy.

## 3. v2 Result Summary

Configuration:

| Item | Value |
|---|---:|
| Seed | 20260616 |
| Holdout ratio | 0.05 |
| Hold-out EC-4 classes | 126 |
| Hold-out rows | 7518 |
| Evaluated hold-out queries | 7513 |
| Skipped hold-out queries | 5 |
| Hold-out corpus mask banned rows | 7518 |
| In-sample subset | 5000 |

Metrics:

| Metric | Hold-out | In-sample 5K | HO/IS ratio | Status |
|---|---:|---:|---:|---|
| EC-3 MRR | 0.618702 | 0.933737 | 0.662609 | PASS |
| EC-3 top-1 | 0.588047 | 0.899000 | 0.654113 | reported |
| EC-3 top-5 | 0.623453 | 0.936200 | 0.665940 | PASS within tolerance |
| EC-3 top-10 | 0.653534 | 0.959600 | 0.681048 | reported |

Teacher references:

- HO EC-3 MRR reference: `>= 0.50`, tolerance `+/-0.05`.
- HO EC-3 top-5 reference: `>= 0.65`, tolerance `+/-0.05`.
- HO/IS MRR ratio reference: `>= 0.65`, tolerance `+/-0.05`.
- Direction check: HO/IS MRR ratio must be `< 1.0`.

Interpretation:

- HO EC-3 MRR passes the nominal reference.
- HO EC-3 top-5 is below nominal `0.65` but passes within tolerance.
- HO/IS MRR ratio passes the nominal reference and has the correct direction.
- All reported HO/IS ratios are below `1.0`.
- v2 supports cross-class EC-family transfer under teacher tolerance.

Expected-range context:

- HO EC-3 MRR `0.618702` is within expected range `0.45-0.75`.
- IS EC-3 MRR `0.933737` is above expected range `0.55-0.85`.
- HO/IS MRR ratio `0.662609` is below expected range `0.70-0.95`, while still
  passing the acceptance reference and direction check.

## 4. v1 Handling

The v1 report and v1 JSON are retained for traceability only.

v1 is not used as cross-EC4-class transfer evidence because:

- held-out EC-4 enzyme corpus rows were not excluded;
- query self rows were not excluded;
- HO/IS MRR ratio was greater than `1.0`, which is the leakage direction
  identified by the teacher.

The retained v1 markdown files are marked as superseded/leaked audit evidence.
The retained v1 JSON conclusion is also marked as a superseded audit result.

## 5. Linked Document Updates

Updated local/package documents:

- `R3_ACCEPTANCE_NOTE_20260616_173549.md`
- `R3_AGENT_INTEGRATION_PREREQUISITES.md`
- `R3_MODEL_FREEZE_20260616_174232.md`
- package `README.md`
- repository root `README.md`

Update summary:

- Acceptance note now cites v2 as final validation and v1 as leaked/audit only.
- Agent prerequisites keep `score >= 0.9` as the v1 accept threshold and allow
  unseen EC-4 natural fallback under the same score rule using v2
  tolerance-supported evidence.
- Freeze report preserves SHA256, permissions, and frozen artifact evidence;
  only Leave-EC4-Out provenance wording was revised.
- README files point final Leave-EC-Out validation to the v2 report.

## 6. Verification

Compile check:

```text
python3 -m py_compile custom/docs/bio_vector/eval_leave_ec4_out.py \
  enzyme-cage-bio-vector-demo/06_r3_agent_ready_package_20260616/eval_leave_ec4_out.py
```

Result: passed.

Old-claim search:

No package/root README hits remain for old v1 final-claim wording, including
the prior robust-transfer phrasing, the prior all-thresholds-passed phrasing,
the prior v1-MRR decision expression, or final Leave-EC-Out links pointing to
the v1 report.

Forbidden-action search:

No positive declarations were found for:

- `train.py modified: yes`
- `sbatch executed: yes`
- `GPU/DCU used: yes`
- `retraining executed: yes`
- `R4 opened: yes`

## 7. Declarations

| Item | Status |
|---|---|
| `train.py` modified | no |
| retraining executed | no |
| GPU/DCU used by local package update | no |
| Slurm submitted by local package update | no |
| R4 opened | no |
| local package files checked | yes |
| local package old-claim search passed | yes |
| remote GitHub pre-update checked | yes; `origin/main` was still the old v1 package at commit `1e990dc` |
| remote GitHub post-update checked | pending after push |
| HPC output path rechecked | no, requires separate HPC-side command |

## 8. Next Checks

Before declaring remote delivery complete:

1. Push this package update to GitHub and verify the remote package contains the
   same v2 files and revised wording.
2. If needed, ask HPC to confirm the authoritative output directory with
   `ls -lh`, `python -m py_compile`, and file paths for the v2 report/JSON.
