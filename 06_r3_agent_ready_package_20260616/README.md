# R3 Agent-Ready Package 2026-06-16

This folder contains the final teacher-facing R3 acceptance and agent-readiness
package after the 2026-06-16 Leave-EC4-Out validation.

## Contents

| File | Purpose |
|---|---|
| `eval_leave_ec4_out.py` | Final zero-GPU Leave-EC4-Out evaluation script. |
| `R3_LEAVE_EC4_OUT_20260616_171432.md` | Final Leave-EC4-Out validation report. |
| `r3_leave_ec4_out.json` | Raw Leave-EC4-Out audit data, including rank lists and per-EC4-class summaries. |
| `R3_ACCEPTANCE_NOTE_20260616_173549.md` | Final R3 acceptance note with teacher rating revisions. |
| `R3_MODEL_FREEZE_20260616_174232.md` | HPC model-freeze evidence for `frozen/model_v3.pt`. |
| `R3_AGENT_INTEGRATION_PREREQUISITES.md` | Agent integration prerequisites and policy constraints. |

## Final Status

- R3 is accepted as the current `tool/verifier` candidate.
- Leave-EC4-Out validation passed all teacher reference checks.
- R3 model freeze was completed with checksum evidence.
- Agent v1 policy uses `score >= 0.9` to accept top-1 and abstains otherwise.
- No R4 training, no retraining, no `train.py` modification, and no real OOD
  data collection are included in this package.
