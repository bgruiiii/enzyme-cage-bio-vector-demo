# R3 Retrieval Toolkit Checklist Execution Log

Generated: 2026-06-17

Scope: local GitHub demo repository preparation for
`07_r3_retrieval_toolkit_2026-06-17/`.

Boundary declarations:

- No API server implemented.
- No LLM or agent reranking implemented.
- No R3 retraining executed.
- No R4 work opened.
- `train.py` was not modified.
- `torch`, `transformers`, `sklearn`, `faiss`, and `hnswlib` were not added to
  runtime requirements.
- Large artifacts `model_v3.pt`, `embeddings_v3.npz`, and `metadata_v3.json`
  were not copied into the GitHub demo repo.

## RULE Status

| Rule | Status | Evidence |
|---|---|---|
| RULE-1 directory skeleton | PASS | Created package, tests, examples, and data directories. |
| RULE-2 loader.py | PASS | `load_artifacts()` loads `embeddings_v3.npz` and `metadata_v3.json`, returns L2-normalized float32 embeddings and metadata. |
| RULE-3 retrieval.py | PASS | Implemented `r2e_retrieval`, `e2m_retrieval`, `s2m_retrieval`; numpy only; query normalization; descending score; 1-indexed rank; optional self-row and EC-4 exclusion for R2E. |
| RULE-4 metadata.py | PASS | Implemented `lookup_metadata`, `is_known_ec4`, `get_ec3_neighbors`, and cached one-pass EC index. |
| RULE-5 examples | PASS on lightweight fixture | Six scripts run with `--output_dir` on a temporary fixture; real R3 examples are runnable with the final R3 HPC output path but were not rerun locally because the large artifacts are intentionally not copied into this repo. |
| RULE-6 pytest | PASS locally and on real R3 HPC artifacts | Local: 9 passed, 1 skipped. HPC real artifacts: 10 passed in 7.14s. |
| RULE-7 data/README.md | PASS | Documents excluded large files, verified R3 HPC file sizes, final R3 HPC output path, and `--output_dir` usage. |
| RULE-8 requirements.txt | PASS | Contains exactly `numpy>=1.26.0` and `pytest>=7.0.0`; no forbidden runtime dependencies. |
| RULE-9 README.md | PASS | Includes positioning, data prep with final HPC path, six API examples, performance table, agent gating template, open-domain query boundary, and real-R3 RULE-6 pytest result. |
| RULE-10 MODEL_ARCHITECTURE.md | PASS | YAML parses locally; HPC state_dict audit confirmed frozen checkpoint SHA256, reaction_projector key order/shapes, allowed BatchNorm extra keys, and documented layer order. |
| RULE-11 export r3_reaction_encoder.npz | PASS | HPC export produced `data/r3_reaction_encoder.npz` with sha256 `1857a179f255130e3b561c76f8c752b93e58c423cc5c7e3187e9fa34db0b1e5c`; row-0 numpy-forward cosine `1.00000000` passed `>= 0.9999`; local toolkit copy matches sha256. |
| RULE-12 this log | PASS | Final audit completed; this file records actual outputs, deviations, HPC evidence, verification status, encoder export details, and RULE-13 upload scope. |
| RULE-13 git commit/push | PASS | Prepared for commit/push from `main` to `origin/main`; pre-upload git status contains only `.gitignore`, repository `README.md`, and `07_r3_retrieval_toolkit_2026-06-17/`. |

## Local Verification Commands

```text
python3 -m pytest tests/ -v
python3 -m compileall -q r3_retrieval examples tests
```

Pytest result:

```text
collected 10 items
tests/test_loader.py::test_load_artifacts PASSED
tests/test_loader.py::test_real_r3_artifacts_shape_when_available SKIPPED
tests/test_metadata.py::test_lookup_metadata_hit_and_miss PASSED
tests/test_metadata.py::test_unseen_ec4_returns_false PASSED
tests/test_metadata.py::test_get_ec3_neighbors PASSED
tests/test_metadata.py::test_empty_metadata_fields_fallback_to_unknown PASSED
tests/test_retrieval.py::test_r2e_self_query_top1_score_high PASSED
tests/test_retrieval.py::test_r2e_returns_dataclass_with_metadata PASSED
tests/test_retrieval.py::test_r2e_exclusion_controls PASSED
tests/test_retrieval.py::test_e2m_and_s2m_return_candidate_sets PASSED
9 passed, 1 skipped
```

## RULE-6 HPC Real Artifact Verification

HPC result files reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/bio_vector/RULE6_HPC_REAL_ARTIFACT_PYTEST_20260617.md
/home/a/EnzymeCAGE/custom/docs/bio_vector/RULE6_HPC_PYTEST_RAW_20260617.txt
```

HPC paths:

```text
toolkit_dir: /public/home/acfbwjsi7s/07_r3_retrieval_toolkit_2026-06-17
R3_ARTIFACT_DIR: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15
embeddings_v3.npz: 569M
metadata_v3.json: 22M
```

HPC environment:

```text
Python 3.9.23
numpy 1.26.4
pytest 8.4.2
host login07
```

HPC pytest result:

```text
tests/test_loader.py::test_real_r3_artifacts_shape_when_available PASSED
10 passed in 7.14s
exit code 0
```

HPC declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used: no
Slurm submitted: no
R4 opened: no
large artifacts copied into toolkit repo: no
```

Compile result:

```text
python3 -m compileall -q r3_retrieval examples tests
exit code 0
```

## RULE-10 HPC Model Architecture Audit

HPC result file reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/RULE10_HPC_MODEL_ARCHITECTURE_STATE_DICT_AUDIT_20260617.md
```

HPC paths:

```text
toolkit_dir: /public/home/acfbwjsi7s/07_r3_retrieval_toolkit_2026-06-17
architecture_md: /public/home/acfbwjsi7s/07_r3_retrieval_toolkit_2026-06-17/data/MODEL_ARCHITECTURE.md
frozen_checkpoint: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/frozen/model_v3.pt
```

Checkpoint SHA256:

```text
expected: f728455ecc9d12c1eb3fc084fdc5445933befa5b7eb56a3644965fb4e0519c4c
actual:   f728455ecc9d12c1eb3fc084fdc5445933befa5b7eb56a3644965fb4e0519c4c
match:    True
```

Architecture audit result:

```text
parser: torch-free pure-python parser, because torch was unavailable on the
        login node due to a HIP runtime library issue.
reaction_projector expected shape checks: all PASS
allowed BatchNorm extra keys: present
MODEL_ARCHITECTURE.md missing required phrases: []
MODEL_ARCHITECTURE.md documented layer order ok: True
missing state_dict keys: []
shape mismatches: []
unexpected reaction_projector keys: []
RULE-10 pass: True
```

Audited reaction projector shapes:

```text
reaction_projector.net.0.weight: (512, 2048)
reaction_projector.net.0.bias: (512,)
reaction_projector.net.1.weight/bias/running_mean/running_var: (512,)
reaction_projector.net.3.weight: (512, 512)
reaction_projector.net.3.bias: (512,)
reaction_projector.net.4.weight/bias/running_mean/running_var: (512,)
reaction_projector.net.6.weight: (256, 512)
reaction_projector.net.6.bias: (256,)
```

HPC declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used: no
Slurm submitted: no
R4 opened: no
r3_reaction_encoder.npz exported in RULE-10: no
```

Final local verification after RULE-11:

```text
python3 -m pytest tests/ -v
9 passed, 1 skipped in 0.20s

python3 -m compileall -q r3_retrieval examples tests
exit code 0

sha256sum data/r3_reaction_encoder.npz
1857a179f255130e3b561c76f8c752b93e58c423cc5c7e3187e9fa34db0b1e5c
```

Large-artifact negative check:

```text
find ... -name embeddings_v3.npz -o -name metadata_v3.json -o -name model_v3.pt
no matches
```

Cache cleanup:

```text
No __pycache__ or .pytest_cache directories are retained after final checks.
```

## Example Smoke-Test Output

The six examples were run against a temporary 3-row fixture to verify entry
points and API wiring. This is not R3 evidence.

```text
01_r2e_basic.py:
R2E top-5 for metadata row 0
1 1.000000 P00001 1.14.13.1 Example monooxygenase
top1_score=1.000000

02_e2m_candidate_set.py:
WARNING: E2M top-1 is about 0.006; use top_k as a candidate set.
E2M candidates=3

03_s2m_candidate_set.py:
WARNING: S2M top-1 is about 0.006; use top_k as a candidate set.
S2M candidates=3

04_metadata_lookup.py:
lookup_uniprot=P00001
{'uniprot_id': 'P00001', 'ec_number': '1.14.13.1', ...}

05_unseen_ec4_abstain.py:
abstain due to unseen EC-4

06_ec_classification.py:
predicted_ec4=1.14.13.1
top10_votes={'1.14.13.1': 1, '1.14.13.2': 1, '2.7.1.1': 1}
```

## RULE-11 HPC Reaction Encoder Export

HPC result files reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/RULE11_HPC_REACTION_ENCODER_EXPORT_20260617.md
/home/a/EnzymeCAGE/custom/docs/RULE11_HPC_REACTION_ENCODER_EXPORT_RAW_20260617.txt
```

HPC export path:

```text
/public/home/acfbwjsi7s/07_r3_retrieval_toolkit_2026-06-17/data/r3_reaction_encoder.npz
```

Local toolkit copy:

```text
/home/a/EnzymeCAGE/enzyme-cage-bio-vector-demo/07_r3_retrieval_toolkit_2026-06-17/data/r3_reaction_encoder.npz
```

Export evidence:

```text
loader: torch-free zip/pickle parser
checkpoint sha256 match: true
export sha256: 1857a179f255130e3b561c76f8c752b93e58c423cc5c7e3187e9fa34db0b1e5c
export size: 5.6M
row-0 numpy-forward cosine: 1.00000000
threshold: >= 0.9999
RULE-11 pass: true
```

Exported arrays:

```text
linear0_weight [512, 2048]
linear0_bias [512]
bn1_weight [512]
bn1_bias [512]
bn1_running_mean [512]
bn1_running_var [512]
linear3_weight [512, 512]
linear3_bias [512]
bn4_weight [512]
bn4_bias [512]
bn4_running_mean [512]
bn4_running_var [512]
linear6_weight [256, 512]
linear6_bias [256]
eps []
```

Declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used: no
Slurm submitted: no
R4 opened: no
model_v3.pt copied/uploaded: no
embeddings_v3.npz copied/uploaded: no
metadata_v3.json copied/uploaded: no
```

## Deviations

- Full real-data pytest with `N=145607` was run on HPC through
  `R3_ARTIFACT_DIR=/path/to/r3/output python -m pytest tests/ -v` and passed.
- Full real-data examples were not rerun locally because `embeddings_v3.npz`
  and `metadata_v3.json` are intentionally not copied into the GitHub demo repo.
  The examples accept `--output_dir` and can be run against the final R3 HPC
  output directory.
- `.gitignore` has a narrow exception so
  `07_r3_retrieval_toolkit_2026-06-17/data/r3_reaction_encoder.npz` is allowed
  for commit; other `.npz` files remain ignored.

## RULE-12 Final Audit Verdict

RULE-1 through RULE-12 are complete. RULE-13 upload scope was reviewed before
staging. The commit/push step includes only the intended toolkit files plus the
required `.gitignore` and repository README updates.

Final inclusion check:

```text
include: 07_r3_retrieval_toolkit_2026-06-17/**
include: 07_r3_retrieval_toolkit_2026-06-17/data/r3_reaction_encoder.npz
exclude: model_v3.pt
exclude: embeddings_v3.npz
exclude: metadata_v3.json
exclude: __pycache__/
exclude: .pytest_cache/
```

RULE-13 pre-upload git status:

```text
 M .gitignore
 M README.md
?? 07_r3_retrieval_toolkit_2026-06-17/
```

Interpretation:

```text
Only the intended repository README update, .gitignore exception, and new
toolkit directory are present before staging.
```

RULE-13 commit metadata:

```text
branch: main
remote: origin git@github.com:bgruiiii/enzyme-cage-bio-vector-demo.git
commit message: R3 retrieval toolkit v1: numpy retrieval + reaction encoder weights for open-domain query
```
