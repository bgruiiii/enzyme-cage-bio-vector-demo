# R3 Teacher Submission Manifest

Date: 2026-06-15

Scope: final cleaned R3 submission package. This package intentionally excludes
older planning drafts, intermediate diffs, and working notes.

## Checklist Mapping

| Teacher checklist item | Package file(s) | Status |
|---|---|---|
| 3.1 R2 final addenda | `R2_POSTMORTEM_20260615_FINAL.md` | Present |
| 3.1 R2 EC-4 bucket baseline | `R2_EC4_BUCKET_BASELINE.md` | Present |
| 3.1 bucket eval script | `eval_ec4_buckets.py` | Present; has docstring, `--checkpoint`, `--output_dir`, `--report_path`, `--chunk_size` |
| 3.2 R3 code changes | `R3_RESULT_SUMMARY_20260615.md` | Summarized with audited final config and stage3 alias |
| 3.3 R3 training artifacts | `R3_TRAIN_COMPLETION_AUDIT_20260615.md`, `R3_RESULT_SUMMARY_20260615.md` | Present |
| 3.4 R3 result summary | `R3_RESULT_SUMMARY_20260615.md` | Present |
| 3.4 bucket table | `R3_RESULT_SUMMARY_20260615.md`, `R3_EC4_BUCKET_EVAL_20260615.md` | Present |
| 3.4 criteria table | `R3_RESULT_SUMMARY_20260615.md` | Present, PASS/FAIL table included |
| 3.4 stage-wise checkpoint MRR | `R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md`, `postmortem_eval_stage_checkpoints.py` | Present |
| 3.4 training time comparison | `R3_RESULT_SUMMARY_20260615.md` | Present |
| 3.5 R4 decision input | `R4_DECISION_INPUT.md` | Present; decision input only, no R4 plan details |

## Packaged Files

```text
R2_POSTMORTEM_20260615_FINAL.md
R2_EC4_BUCKET_BASELINE.md
eval_ec4_buckets.py
postmortem_eval_stage_checkpoints.py
R3_TRAIN_COMPLETION_AUDIT_20260615.md
R3_METRICS_COMPARISON_AUDIT_20260615.md
R3_EC4_BUCKET_EVAL_20260615.md
R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md
R3_RESULT_SUMMARY_20260615.md
R4_DECISION_INPUT.md
```

## Final Checks

| Check | Result |
|---|---|
| Final candidate file existence | PASS |
| `eval_ec4_buckets.py` py_compile | PASS |
| `postmortem_eval_stage_checkpoints.py` py_compile | PASS |
| Final candidate guarded-wording search | PASS |
| `R4_DECISION_INPUT.md` contains R4 plan details | No |
| Entire working directory included | No |

## Notes

- `R3_RESULT_SUMMARY_20260615.md` records that the main EC-4 grouped retrieval
  metric passed the teacher criterion.
- `R3_RESULT_SUMMARY_20260615.md` also records two criteria as not attained:
  EC-4 tail bucket target margin and training-time target.
- `R4_DECISION_INPUT.md` is a decision input only. It intentionally avoids
  implementation configuration details.
