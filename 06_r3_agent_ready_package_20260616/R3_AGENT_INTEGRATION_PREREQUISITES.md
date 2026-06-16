# R3 Agent Integration Prerequisites

**Date**: 2026-06-16  
**Scope**: Required agent-side policy before using the accepted R3
`tool/verifier` model.  
**Model state**: R3 accepted and frozen. No R4 training is opened.

## 1. Required Inputs

| Artifact | Status |
|---|---|
| R3 accepted as current `tool/verifier` candidate | complete |
| R3 model freeze | complete |
| Leave-EC4-Out validation | complete, 5/5 thresholds PASS |
| Agent-side calibration implementation | not delivered in this package |
| Real OOD data collection | not delivered in this package |

中文说明：本文只写 agent 接入前的策略约束，不实现新训练、不实现 recalibration、不收集真实 OOD 数据。

## 2. Confidence Threshold Strategy

Agent integration v1 must use a simple acceptance/abstention rule:

```text
score >= 0.9 -> accept top-1 candidate
score < 0.9  -> abstain
```

| Score range | Approx. bin share | Calibration state | Agent v1 action |
|---|---:|---|---|
| 0.9-1.0 | 88% | close to diagonal, gap +0.054 | accept top-1, confidence = score |
| 0.8-0.9 | 12% | over-confident, gap +0.485 | abstain in v1; do not use raw confidence |
| < 0.8 | <0.1% | very sparse support | abstain |

Required concrete threshold:

```text
accept_threshold = 0.9
```

Operational notes:

- The accepted result is the top-1 candidate plus its score.
- Scores below `0.9` are not converted into raw confidence in v1.
- Isotonic recalibration is not implemented in this package; it remains an
  optional later agent-side improvement.

中文说明：v1 先用 `score >= 0.9` 这一条硬阈值。0.8-0.9 区间不使用 raw confidence，直接 abstain。

## 3. Unseen EC-4 Fallback Decision

Leave-EC4-Out validation result:

| Metric | Hold-out | In-sample 5K | Ratio | Rating |
|---|---:|---:|---:|---|
| EC-3-grouped MRR | 0.984791 | 0.935949 | 1.052185 | PASS |
| EC-3 top-1 | 0.966879 | 0.889600 | 1.086870 | PASS |
| EC-3 top-5 | 0.984836 | 0.937400 | 1.050604 | PASS |
| EC-3 top-10 | 0.984836 | 0.961000 | 1.024804 | PASS |

Teacher decision rule:

```text
if Leave-EC4-Out EC-3-grouped MRR >= 0.80:
    allow natural fallback to same EC-3 neighbors
else:
    require EC-label lookup; abstain for unseen EC-4 classes
```

Applied to R3:

```text
0.984791 >= 0.80 -> natural EC-3-family fallback is supported
```

Agent v1 decision tree:

```text
input reaction
  |
  v
R3 R->E retrieval
  |
  v
top-1 score >= 0.9 ?
  | yes
  v
accept top-1 candidate
  |
  v
if EC-4 is not present in training classes:
    rely on demonstrated EC-3-family fallback
else:
    use standard in-corpus retrieval behavior

top-1 score < 0.9 ?
  |
  v
abstain
```

中文说明：Leave-EC4-Out 已经通过，agent v1 不需要把 unseen EC-4 直接退化成 lookup-table abstain；只要 top-1 score 达到 0.9，就允许模型自然回落到同 EC-3 family 邻居。

## 4. OOD Detection Staging

OOD detection is staged, not implemented in v1.

| Stage | Policy | Delivered now |
|---|---|---|
| Agent v1 | rely on `score >= 0.9` threshold and abstain below threshold | yes, policy only |
| Agent v2 | collect real non-enzyme reaction examples and implement abstain-on-OOD | no |

Notes:

- R2 postmortem recorded candidate sources for future real OOD data.
- The current synthetic Gaussian proxy is treated as a baseline signal only.
- Agent v1 does not implement a separate OOD detector.
- Agent v2 should evaluate real non-enzyme reaction data before adding an OOD
  abstention module.

中文说明：v1 不做独立 OOD detector，先靠 `score < 0.9 abstain` 兜底。真实 non-enzyme reaction 数据留到 v2 收集和验证。

## 5. Do Not Deliver In This Step

- No R4 plan.
- No calibration recalibration implementation.
- No real OOD data collection.
- No new training run.
- No `train.py` modification.

## 6. Final Agent-Readiness Statement

R3 is ready for agent integration v1 under the following mandatory policy:

```text
Use frozen R3 artifacts.
Use top-1 result only when score >= 0.9.
Abstain when score < 0.9.
Allow unseen EC-4 natural fallback to EC-3-family neighbors, because
Leave-EC4-Out passed with EC-3-grouped MRR = 0.984791.
Do not add OOD detection until agent v2 has real non-enzyme reaction data.
```
