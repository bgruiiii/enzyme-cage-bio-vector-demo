# EnzymeCAGE Bio Vector R3 Results

This repository is a clean review copy of the EnzymeCAGE / Bio Vector Round 3
result package.

It contains the teacher-facing R3 reports, supporting R2 context, evaluation
audits, and reproducibility scripts that were included in the final R3
submission package.

## Summary

Round 3 evaluates Bio Vector as a tool/verifier candidate model for
reaction-to-enzyme retrieval.

Key result files:

- Main R3 summary: [`03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md`](03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md)
- R3 metrics audit: [`03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md`](03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md)
- EC-4 bucket evaluation: [`03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md`](03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md)
- Stage-wise checkpoint evaluation: [`03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md`](03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md)
- Submission manifest: [`00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md`](00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md)

## Repository Layout

```text
00_manifest/
  Final submission manifest.

01_r2_context/
  R2 postmortem context and EC-4 bucket baseline used for R3 comparison.

02_r3_training/
  R3 training completion audit.

03_r3_evaluation/
  R3 result summary and evaluation audits.

04_decision_inputs/
  Archived decision input included in the R3 submission package.

scripts/
  Evaluation scripts archived with the submission.
```

## Included Files

```text
00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md
01_r2_context/R2_POSTMORTEM_20260615_FINAL.md
01_r2_context/R2_EC4_BUCKET_BASELINE.md
02_r3_training/R3_TRAIN_COMPLETION_AUDIT_20260615.md
03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md
03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md
03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md
03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md
04_decision_inputs/R4_DECISION_INPUT.md
scripts/eval_ec4_buckets.py
scripts/postmortem_eval_stage_checkpoints.py
```

## Notes

- This repository does not include raw datasets, model checkpoint weights, or
  large embedding artifacts.
- The files here are organized for review and traceability.
- The evaluation scripts are archived for provenance with the reports.
- Round 3 has been treated as the current tool/verifier candidate state; this
  repository is not a new training plan.

