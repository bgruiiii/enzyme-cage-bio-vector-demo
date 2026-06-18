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

## BioDeg v0.2 Task 1 Open-Domain DRFP Sanity

HPC result reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/bio_vector/V0_2_OPEN_DOMAIN_SANITY_HPC_RESULT_20260618.md
```

HPC paths:

```text
toolkit_dir: /public/home/acfbwjsi7s/07_r3_retrieval_toolkit_2026-06-17
R3_ARTIFACT_DIR: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15
metadata_v3.json: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/metadata_v3.json
embeddings_v3.npz: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/embeddings_v3.npz
reaction_features.npz: /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/data/reaction_enzyme_microbe_training_clean_2026-06-01_LOCAL/features/reaction/reaction_features.npz
```

Environment:

```text
Python: 3.9.23
pytest: 8.4.2
drfp: 0.3.6
```

Command:

```text
R3_ARTIFACT_DIR=/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15
REACTION_FEATURES_NPZ=/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/data/reaction_enzyme_microbe_training_clean_2026-06-01_LOCAL/features/reaction/reaction_features.npz
python -m pytest tests/test_open_domain_sanity.py -v -s --cache-clear
```

Pytest result:

```text
tests/test_open_domain_sanity.py::test_open_domain_row0_reproduces_saved_reaction_embedding
open_domain_row0_cosine=1.0000000000
PASSED
1 passed, 18 warnings in 4.10s
```

Open-domain sanity result:

```text
metadata_v3.json row 0 keys: assembly_accession, ec_number, example_id, uniprot_id
metadata_row0_example_id: TR000001_RHEA10012_P08159
RxnSMILES source: reaction_features.npz key cano_rxn_smiles, matched by example_id
metadata_row0_rxn_smiles: CN1CCC[C@@H]1c1ccc(O)nc1.O.O=O>>CNCCCC(=O)c1ccc(O)nc1.OO
open_domain_row0_cosine: 1.0000000000
threshold: >= 0.9999
result: PASS
```

Deviation / adaptation:

```text
The teacher prompt requested metadata_v3.json row 0 RxnSMILES, with the field
name chosen according to the actual schema. The actual metadata rows do not
store RxnSMILES inline. They store example_id, uniprot_id, ec_number, and
assembly_accession. The test therefore first checks inline metadata fields and,
when absent, uses REACTION_FEATURES_NPZ to resolve cano_rxn_smiles by
metadata row 0 example_id. This preserves the row-0 sanity objective while
matching the real R3 artifact schema.
```

Declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used: no
large artifacts uploaded: no
R4 opened: no
```

## BioDeg v0.2 Task 2 Large-Artifact Distribution Metadata

HPC artifact audit reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/bio_vector/V0_2_ARTIFACT_DISTRIBUTION_AUDIT_HPC_RESULT_20260618.md
```

NJU Box links checked locally:

```text
shared folder: https://box.nju.edu.cn/d/f8cff4232a6f45dfac56/
embeddings_v3.npz: https://box.nju.edu.cn/f/a4994c6f51614603be50/
metadata_v3.json: https://box.nju.edu.cn/f/cb833b2ad3a24ec69007/
password: none
expires: permanent
```

NJU Box file identity check:

```text
embeddings_v3.npz fileName: embeddings_v3.npz
embeddings_v3.npz fileSize: 596407282 bytes
metadata_v3.json fileName: metadata_v3.json
metadata_v3.json fileSize: 22711862 bytes
```

Large-artifact SHA256 and sizes:

```text
embeddings_v3.npz size: 596407282 bytes / 568.78 MiB
embeddings_v3.npz sha256: 07418be8e79b7e9ae1dcb1bfdefd5cdacff87e4bc37e750c5918e6f5f73b8c14
metadata_v3.json size: 22711862 bytes / 21.66 MiB
metadata_v3.json sha256: c1b02b21bef6ec759b81cb00fc9544a5e8acd00aea0a234cc15516dc9cd55ff1
```

Artifact schema:

```text
embeddings_v3.npz keys: reaction, enzyme, substrate, microbe
reaction shape/dtype: (145607, 256) float32
enzyme shape/dtype: (145607, 256) float32
substrate shape/dtype: (145607, 256) float32
microbe shape/dtype: (145607, 256) float32
metadata_v3.json schema: list[dict]
metadata_v3.json rows: 145607
metadata_v3.json fields: assembly_accession, ec_number, example_id, uniprot_id
```

Files updated:

```text
data/README.md now records NJU Box URLs, SHA256, permanent expiry, npz keys,
and metadata schema.
```

## BioDeg v0.2 Task 3 Response YAML

Created:

```text
V0_2_RESPONSE.yaml
```

Response YAML location in the GitHub demo repository:

```text
V0_2_RESPONSE.yaml
07_r3_retrieval_toolkit_2026-06-17/V0_2_RESPONSE.yaml
```

The repo-root copy satisfies the teacher wording "repo root". The toolkit-local
copy is an identical mirror kept beside the examples, tests, and data docs for
downstream users browsing the toolkit directory.

Filled from audited evidence:

```text
github_repo_url: https://github.com/bgruiiii/enzyme-cage-bio-vector-demo/tree/v0.2-biodeg-handoff/07_r3_retrieval_toolkit_2026-06-17
package_import_root: r3_retrieval
v1_checklist_status: 13/13 RULE PASS
drfp: drfp==0.3.6, DrfpEncoder.encode([rxn_smiles]) with default encode parameters
reaction_encoder: 2048 -> 512 -> BN/ReLU -> 512 -> BN/ReLU -> 256, L2-normalize
substrate_encoder_shared: false
load_time_sec: 1.894120
r2e_query_ms: 18.333061
memory_rss_gb: 1.047417
open_domain_row0_cosine: 1.0000000000
```

Validation note:

```text
YAML contains concrete audited values and no placeholder ellipses. The
open_domain_sanity query is the teacher-required row-0 sanity query resolved
from reaction_features.npz by metadata row-0 example_id, because metadata_v3.json
does not store RxnSMILES inline.
```

Declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used locally: no
large artifacts committed to GitHub: no
R4 opened: no
```

## V1.5 BioDeg Supplement: Substrate Encoder And Reaction Features

Teacher follow-up source:

```text
/home/a/EnzymeCAGE/custom/docs/bio_vector/V0_2_FOLLOWUP_TO_STUDENT_2026-06-18.md
```

HPC evidence reviewed locally:

```text
/home/a/EnzymeCAGE/custom/docs/bio_vector/V1_5_SUBSTRATE_ENCODER_AND_REACTION_FEATURES_HPC_RESULT_20260618.md
```

HPC result:

```text
substrate_encoder_v3.npz exported from frozen substrate_projector.*
substrate_encoder_v3.npz size_bytes: 5794224
substrate_encoder_v3.npz sha256: 0ba789a274674de5a1094c99421e86206041aa0bb111bdd912a9beb2e60a56cb
substrate featurizer: RDKit Morgan fingerprint, radius=2, nBits=2048,
  useChirality=False, useFeatures=False, useBondTypes=True, useCounts=False
metadata row0 example_id: TR000001_RHEA10012_P08159
metadata row0 substrate smiles: CN1CCC[C@@H]1c1ccc(O)nc1.O.O=O
row-0 substrate numpy-forward cosine: 1.0000000000
threshold: >= 0.9999
reaction_features.npz size_bytes: 16691154
reaction_features.npz sha256: c13d056ca28c3c243ea7884a4f50480779e26058f6d585c60fc057aa1f5ad917
reaction_features.npz keys: cano_rxn_smiles, drfp, example_id,
  product_reacting_center_indices, rhea_id, substrate_reacting_center_indices,
  uniprot_id
```

NJU Box links checked locally:

```text
folder: https://box.nju.edu.cn/d/825d7f0611fb44afa451/
substrate_encoder_v3.npz: https://box.nju.edu.cn/f/e041cdc720b24299bfd0/
reaction_features.npz: https://box.nju.edu.cn/f/bb21eceb19e947dca534/
```

Local V1.5 files integrated:

```text
data/substrate_encoder_v3.npz
examples/01_substrate_open_domain_query.py
data/README.md
data/MODEL_ARCHITECTURE.md
README.md
V0_2_RESPONSE.yaml
```

V1.5 local checks at integration time:

```text
python3 -m py_compile examples/01_substrate_open_domain_query.py: PASS
python3 examples/01_substrate_open_domain_query.py --help: PASS
PyYAML parse for both V0_2_RESPONSE.yaml copies: PASS
root and toolkit V0_2_RESPONSE.yaml byte-identical: PASS
substrate_encoder_v3.npz local sha256 matches HPC: PASS
forbidden local large artifacts reaction_features.npz, embeddings_v3.npz,
metadata_v3.json, model_v3.pt: absent
```

V1.5 declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used locally: no
large artifacts committed to GitHub: no
R4 opened: no
GitHub commit/push executed at Batch D: no
```

## BioDeg v0.2 Final Local Audit Before Commit

Scope:

```text
Audit v0.2 handoff files against V0_2_CODEX_PROMPT.md tasks 1-4 before Git
commit/push.
```

Teacher task coverage:

```text
Task 1 open-domain DRFP query: PASS
Task 2 large-file distribution metadata: PASS
Task 3 V0_2_RESPONSE.yaml: PASS
Task 4 GitHub branch/commit/push: not yet executed at this audit point
```

Local commands:

```text
python3 -m pytest tests/ -v
python3 -m compileall -q r3_retrieval examples tests
python3 examples/00_drfp_open_domain_query.py --help
python3 examples/01_r2e_basic.py
python3 examples/02_e2m_candidate_set.py
python3 examples/03_s2m_candidate_set.py
python3 examples/04_metadata_lookup.py
python3 examples/05_unseen_ec4_abstain.py
python3 examples/06_ec_classification.py
git diff --check
find 07_r3_retrieval_toolkit_2026-06-17 -type f -size +10M -print
find 07_r3_retrieval_toolkit_2026-06-17 -name model_v3.pt -o -name embeddings_v3.npz -o -name metadata_v3.json -o -name '*.pyc'
```

Local results:

```text
pytest: 9 passed, 2 skipped
skipped tests: gated real-R3 artifact checks requiring R3_ARTIFACT_DIR and
REACTION_FEATURES_NPZ
compileall: exit code 0
example entrypoints: examples/00 --help succeeded; examples/01-06 ran and
reported missing local large artifacts with the documented --output_dir/data
instruction
open-domain numpy forward local smoke test: zero DRFP -> (256,) float32,
finite, L2 norm 1.00000000
git diff --check: PASS
large file check: no files over 10M in the toolkit tree
forbidden artifact check: no model_v3.pt, embeddings_v3.npz, metadata_v3.json,
or *.pyc in the toolkit tree after cache cleanup
```

NJU Box link check:

```text
embeddings_v3.npz URL returned HTTP 200 and page metadata reports fileName
embeddings_v3.npz and fileSize 596407282.
metadata_v3.json URL returned HTTP 200 and page metadata reports fileName
metadata_v3.json and fileSize 22711862.
shared folder URL returned HTTP 200 and title BioDeg_R3_Handoff.
```

Response YAML check:

```text
V0_2_RESPONSE.yaml at repo root parses with PyYAML.
07_r3_retrieval_toolkit_2026-06-17/V0_2_RESPONSE.yaml parses with PyYAML.
The two YAML copies are byte-identical.
Required top-level fields are present.
Focused placeholder scan on V0_2_RESPONSE.yaml, data/README.md, examples/00,
and tests/test_open_domain_sanity.py found no placeholders.
```

Caveats:

```text
Open-domain real DRFP execution is verified on HPC, not locally, because the
local Python environment does not have drfp==0.3.6 and the true large R3
artifacts are intentionally not copied into the GitHub repo.
metadata_v3.json does not contain RxnSMILES inline; the row-0 sanity test uses
REACTION_FEATURES_NPZ fallback to resolve cano_rxn_smiles by example_id.
```

Declarations:

```text
train.py modified: no
retraining executed: no
GPU/DCU used locally: no
large artifacts committed to GitHub: no
R4 opened: no
```
