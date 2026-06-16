# EnzymeCAGE Bio Vector Demo

This repository is a clean review copy of the EnzymeCAGE / Bio Vector demo and
evaluation evidence.

It contains teacher-facing reports, supporting R2 context, R3 evaluation audits,
Leave-EC-Out generalization validation, and reproducibility scripts.

## Summary

Bio Vector is evaluated as a tool/verifier candidate model for
reaction-to-enzyme retrieval in the EnzymeCAGE workflow.

Key result files:

- R2 postmortem report: [`01_r2_postmortem_submission/R2_POSTMORTEM_20260614.md`](01_r2_postmortem_submission/R2_POSTMORTEM_20260614.md)
- R2 result summary: [`01_r2_postmortem_submission/BIO_VECTOR_R2_RESULT_SUMMARY_2026-06-11.md`](01_r2_postmortem_submission/BIO_VECTOR_R2_RESULT_SUMMARY_2026-06-11.md)
- Main R3 summary: [`03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md`](03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md)
- R3 metrics audit: [`03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md`](03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md)
- EC-4 bucket evaluation: [`03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md`](03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md)
- Stage-wise checkpoint evaluation: [`03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md`](03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md)
- Leave-EC-Out validation: [`05_leave_ec_out_generalization/R3_LEAVE_EC4_OUT_20260616_165840.md`](05_leave_ec_out_generalization/R3_LEAVE_EC4_OUT_20260616_165840.md)
- Submission manifest: [`00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md`](00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md)

## Latest Generalization Check

The Leave-EC4-Class-Out validation uses saved R3 embeddings only. It holds out
5% of EC-4 classes and evaluates EC-3-grouped reaction-to-enzyme retrieval.

| Metric | Hold-out | In-sample 5K | Ratio |
|---|---:|---:|---:|
| EC-3 MRR | 0.984791 | 0.935949 | 1.052185 |
| EC-3 top-1 | 0.966879 | 0.889600 | 1.086870 |
| EC-3 top-5 | 0.984836 | 0.937400 | 1.050604 |
| EC-3 top-10 | 0.984836 | 0.961000 | 1.024804 |

The validation report records all teacher reference checks as passing.

## Repository Layout

```text
00_manifest/
  Final submission manifest.

01_r2_postmortem_submission/
  Original R2 postmortem teacher submission files.

01_r2_context/
  R2 context and EC-4 bucket baseline used for R3 comparison.

02_r3_training/
  R3 training completion audit.

03_r3_evaluation/
  R3 result summary and evaluation audits.

04_decision_inputs/
  Archived decision input included in the R3 submission package.

05_leave_ec_out_generalization/
  Leave-EC-Out generalization validation report, JSON output, and script audits.

scripts/
  Evaluation scripts archived with the submission.
```

## Included Files

```text
00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md
01_r2_postmortem_submission/R2_POSTMORTEM_20260614.md
01_r2_postmortem_submission/BIO_VECTOR_R2_RESULT_SUMMARY_2026-06-11.md
01_r2_postmortem_submission/postmortem_eval_stage_checkpoints.py
01_r2_postmortem_submission/R3_DECISION_INPUT.md
01_r2_context/R2_POSTMORTEM_20260615_FINAL.md
01_r2_context/R2_EC4_BUCKET_BASELINE.md
02_r3_training/R3_TRAIN_COMPLETION_AUDIT_20260615.md
03_r3_evaluation/R3_METRICS_COMPARISON_AUDIT_20260615.md
03_r3_evaluation/R3_EC4_BUCKET_EVAL_20260615.md
03_r3_evaluation/R3_STAGEWISE_CHECKPOINT_EVAL_20260615.md
03_r3_evaluation/R3_RESULT_SUMMARY_20260615.md
04_decision_inputs/R4_DECISION_INPUT.md
05_leave_ec_out_generalization/R3_LEAVE_EC4_OUT_20260616_165840.md
05_leave_ec_out_generalization/r3_leave_ec4_out.json
05_leave_ec_out_generalization/eval_leave_ec4_out.py
scripts/eval_ec4_buckets.py
scripts/postmortem_eval_stage_checkpoints.py
```

## Notes

- This repository does not include raw datasets, model checkpoint weights, or
  large embedding artifacts.
- The files here are organized for review and traceability.
- The evaluation scripts are archived for provenance with the reports.
- This repository is not a new training plan.
