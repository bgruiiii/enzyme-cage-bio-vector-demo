# R4 Decision Input

Date: 2026-06-15

Scope: one-page decision input for teacher review. This is not an experiment
protocol and does not contain R4 training-plan details.

Provenance: prepared locally from the completed R3 result summary and audited
R3 evaluation reports. No new computation or external job was performed for
this document.

## Evidence From R3

| Diagnostic | Key evidence | Implication |
|---|---|---|
| Primary EC-4 retrieval | EC-4-grouped R->E MRR: R2 `0.91321`, R3 `0.91840` | Main project-facing retrieval metric improved |
| Cross-modal monitor | E->M MRR: R2 `0.61955`, R3 `0.61567`; teacher monitor target `>=0.6100` | Enzyme-to-microbe evidence remains within the monitored range |
| EC-2 grouped monitor | EC-2-grouped R->E MRR: R2 `0.93065`, R3 `0.93800` | Coarser EC-level retrieval is preserved |
| Tail bucket | EC-4 tail MRR: R2 `0.904378`, R3 `0.943734`; relative change `+4.35%`, target `+5%` | Long-tail direction improved, but did not reach the teacher target |
| Head bucket | EC-4 head MRR: R2 `0.915733`, R3 `0.922084`; guardrail target `>=0.888261` | Head bucket is preserved under the R3 sampler |
| Training time | R2 `03:24:55`, R3 `03:23:28`; teacher time target `<03:00:00` | Stage3 skip did not produce the expected end-to-end time reduction |
| Stage-wise evidence | stage1 EC-4 MRR `0.925248`, stage2 `0.924295`, stage3 alias `0.924295` | Most R3 alignment is established by stage1; stage3 alias behaves as intended |

## Decision Table

| Decision signal | Candidate direction | Triggered by R3 data? |
|---|---|---|
| Primary EC-4 grouped MRR improved | Consider R3 as the current verifier/tool candidate for EC-4 grouped retrieval | Yes |
| Tail bucket improved but is below the +5% target | Decide whether the next work should focus on long-tail evidence before agent integration | Yes |
| Head bucket guardrail is satisfied | Do not rollback solely for head-bucket preservation reasons | Yes |
| E->M monitor remains within target | Keep enzyme-to-microbe evidence in the tool/verifier interface | Yes |
| Runtime target was not reached | Treat runtime benefit as unresolved; do not claim stage3 skip delivered the expected wall-time reduction | Yes |
| Row-level R->E remains ceiling-bound | Keep row-level exact retrieval as a reference diagnostic, not the project-facing objective | Yes |

## Suggested Teacher Choice

R3 gives a mixed decision signal:

1. The main EC-4 grouped retrieval metric, E->M monitor, EC-2 monitor, and head
   bucket guardrail are satisfied.
2. The long-tail bucket moved in the intended direction but is slightly below
   the teacher target.
3. The wall-time target was not reached in the recorded Slurm run.

The most direct teacher decision is between:

1. Proceed to limited agent/tool integration using R3 as the current EC-4
   verifier candidate, while clearly carrying the tail and runtime findings as
   unresolved evidence items.
2. Run one more teacher-approved round focused on the two unmet R3 criteria:
   long-tail bucket margin and end-to-end runtime accounting.
3. Keep R2 as the conservative reference and use R3 only as evidence that
   class-balanced sampling can improve EC-4 grouped MRR without reducing the
   head bucket.

This document intentionally avoids implementation configuration details. Those
should be written only after the teacher selects a direction.
