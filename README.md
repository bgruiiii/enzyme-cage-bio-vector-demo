# EnzymeCAGE Bio Vector Demo

This repository is a clean review copy of the EnzymeCAGE / Bio Vector demo and
evaluation evidence.

It contains teacher-facing reports, supporting R2 context, R3 evaluation audits,
Leave-EC-Out generalization validation, R3 acceptance/freeze evidence, agent
integration prerequisites, and reproducibility scripts.

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
- Final R3 agent-ready package: [`06_r3_agent_ready_package_20260616/`](06_r3_agent_ready_package_20260616/)
- Final Leave-EC-Out validation: [`06_r3_agent_ready_package_20260616/R3_LEAVE_EC4_OUT_v2_20260617_001330.md`](06_r3_agent_ready_package_20260616/R3_LEAVE_EC4_OUT_v2_20260617_001330.md)
- R3 acceptance note: [`06_r3_agent_ready_package_20260616/R3_ACCEPTANCE_NOTE_20260616_173549.md`](06_r3_agent_ready_package_20260616/R3_ACCEPTANCE_NOTE_20260616_173549.md)
- R3 model freeze evidence: [`06_r3_agent_ready_package_20260616/R3_MODEL_FREEZE_20260616_174232.md`](06_r3_agent_ready_package_20260616/R3_MODEL_FREEZE_20260616_174232.md)
- Agent integration prerequisites: [`06_r3_agent_ready_package_20260616/R3_AGENT_INTEGRATION_PREREQUISITES.md`](06_r3_agent_ready_package_20260616/R3_AGENT_INTEGRATION_PREREQUISITES.md)
- Final package audit: [`06_r3_agent_ready_package_20260616/R3_AGENT_READY_PACKAGE_V2_LEAKFIX_AUDIT_20260617.md`](06_r3_agent_ready_package_20260616/R3_AGENT_READY_PACKAGE_V2_LEAKFIX_AUDIT_20260617.md)
- Submission manifest: [`00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md`](00_manifest/R3_TEACHER_SUBMISSION_MANIFEST_20260615.md)

## Final R3 Agent-Ready Package

The final 2026-06-16 package is in
[`06_r3_agent_ready_package_20260616/`](06_r3_agent_ready_package_20260616/).
It contains exactly the final teacher-facing artifacts for R3 acceptance,
Leave-EC-Out v2 validation, model freeze evidence, and agent integration
prerequisites. The original v1 Leave-EC4-Out report is retained only as leaked
row-level self-alignment audit evidence.

## Latest Generalization Check

The final Leave-EC4-Class-Out v2 validation uses saved R3 embeddings only. It
holds out 5% of EC-4 classes and evaluates EC-3-grouped reaction-to-enzyme
retrieval after excluding held-out EC-4 enzyme corpus rows and query self rows.

| Metric | Hold-out | In-sample 5K | Ratio |
|---|---:|---:|---:|
| EC-3 MRR | 0.618702 | 0.933737 | 0.662609 |
| EC-3 top-1 | 0.588047 | 0.899000 | 0.654113 |
| EC-3 top-5 | 0.623453 | 0.936200 | 0.665940 |
| EC-3 top-10 | 0.653534 | 0.959600 | 0.681048 |

The v2 report records HO EC-3 MRR as a nominal pass, HO EC-3 top-5 as a
tolerance pass, and HO/IS MRR ratio as a nominal pass with the expected
direction (`< 1.0`). This supports cross-class EC-family transfer under teacher
tolerance.

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
  Earlier Leave-EC-Out generalization validation archive.

06_r3_agent_ready_package_20260616/
  Final R3 acceptance, Leave-EC-Out, model-freeze, and agent-readiness package.

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
06_r3_agent_ready_package_20260616/README.md
06_r3_agent_ready_package_20260616/eval_leave_ec4_out.py
06_r3_agent_ready_package_20260616/R3_LEAVE_EC4_OUT_20260616_171432.md
06_r3_agent_ready_package_20260616/R3_LEAVE_EC4_OUT_v1_LEAKED_20260616_171432.md
06_r3_agent_ready_package_20260616/R3_LEAVE_EC4_OUT_v2_20260617_001330.md
06_r3_agent_ready_package_20260616/r3_leave_ec4_out.json
06_r3_agent_ready_package_20260616/r3_leave_ec4_out_v2.json
06_r3_agent_ready_package_20260616/R3_ACCEPTANCE_NOTE_20260616_173549.md
06_r3_agent_ready_package_20260616/R3_MODEL_FREEZE_20260616_174232.md
06_r3_agent_ready_package_20260616/R3_AGENT_INTEGRATION_PREREQUISITES.md
06_r3_agent_ready_package_20260616/R3_AGENT_READY_PACKAGE_V2_LEAKFIX_AUDIT_20260617.md
scripts/eval_ec4_buckets.py
scripts/postmortem_eval_stage_checkpoints.py
```

## Notes

- This repository does not include raw datasets, model checkpoint weights, or
  large embedding artifacts.
- The files here are organized for review and traceability.
- The evaluation scripts are archived for provenance with the reports.
- This repository is not a new training plan.
- The legacy v1 Leave-EC4-Out path may remain for traceability, but the final
  cross-class transfer evidence is the v2 report.
