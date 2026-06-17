# R3 Agent-Ready Package 2026-06-16

This folder contains the final teacher-facing R3 acceptance and agent-readiness
package after the 2026-06-17 Leave-EC4-Out v2 leak-fix validation.

## Contents

| File | Purpose |
|---|---|
| `eval_leave_ec4_out.py` | Final zero-GPU Leave-EC4-Out v2 leak-fix evaluation script. |
| `R3_LEAVE_EC4_OUT_20260616_171432.md` | Legacy v1 path retained for link compatibility; superseded/leaked audit evidence only. |
| `R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md` | v1 leaked audit report; retained for traceability only. |
| `R3_LEAVE_EC4_OUT_v2_20260617_001330.md` | Final v2 Leave-EC4-Out cross-class transfer report. |
| `r3_leave_ec4_out.json` | v1 raw audit data; retained for traceability only. |
| `r3_leave_ec4_out_v2.json` | Final v2 raw audit data, including rank lists and per-EC4-class summaries. |
| `R3_ACCEPTANCE_NOTE_20260616_173549.md` | Final R3 acceptance note with teacher rating revisions. |
| `R3_MODEL_FREEZE_20260616_174232.md` | HPC model-freeze evidence for `frozen/model_v3.pt`. |
| `R3_AGENT_INTEGRATION_PREREQUISITES.md` | Agent integration prerequisites and policy constraints. |
| `R3_AGENT_READY_PACKAGE_V2_LEAKFIX_AUDIT_20260617.md` | Final local package audit and manifest update after v2 leak-fix. |
| `R3_LEAVE_EC4_OUT_v2_FINAL_HPC_EVIDENCE_20260617.md` | Final HPC output-path evidence for v2 artifacts and v1 leaked copy. |

## Final Status

- R3 is accepted as the current `tool/verifier` candidate.
- Leave-EC4-Out v1 is retained as leaked row-level self-alignment audit
  evidence only.
- Leave-EC4-Out v2 supports cross-class EC-family transfer under teacher
  tolerance: HO EC-3 MRR `0.618702`, HO EC-3 top-5 `0.623453`, HO/IS MRR
  ratio `0.662609`, and all HO/IS ratios are below `1.0`.
- R3 model freeze was completed with checksum evidence.
- Agent v1 policy uses `score >= 0.9` to accept top-1 and abstains otherwise.
- No R4 training, no retraining, no `train.py` modification, and no real OOD
  data collection are included in this package.
