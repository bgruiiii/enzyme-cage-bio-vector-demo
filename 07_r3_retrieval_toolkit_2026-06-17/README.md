# R3 Retrieval Toolkit 2026-06-17

R3 enzyme retrieval toolkit, pure numpy, offline, no API server.

This package wraps frozen R3 embeddings for local agent prototyping. It does not
train, retrain, start a server, call an LLM, or upload large artifacts.

## Data Preparation

Read [`data/README.md`](data/README.md) first. The real R3 files
`embeddings_v3.npz` and `metadata_v3.json` are too large for GitHub and must be
copied from the final R3 HPC output directory or supplied with `--output_dir`.

Final R3 HPC output directory:

```text
/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15
```

```bash
pip install -r requirements.txt
python examples/01_r2e_basic.py --output_dir /path/to/r3/output
```

## API Examples

Load artifacts once:

```python
from r3_retrieval import load_artifacts, set_default_artifacts

art = load_artifacts("/path/to/r3/output")
set_default_artifacts(art)
```

Reaction to enzyme:

```python
from r3_retrieval import r2e_retrieval

query = art["reaction_emb"][0]
hits = r2e_retrieval(query, top_k=10, exclude_self_row_index=None)
for hit in hits:
    print(hit.rank, hit.score, hit.uniprot_id, hit.ec_number)
```

Enzyme to microbe candidate set:

```python
from r3_retrieval import e2m_retrieval

hits = e2m_retrieval("P12345", top_k=50)
for hit in hits:
    print(hit.rank, hit.score, hit.assembly_accession)
```

Use E2M top-k as a candidate set, not as a reliable top-1 decision.

Substrate to microbe candidate set:

```python
from r3_retrieval import s2m_retrieval

query = art["substrate_emb"][0]
hits = s2m_retrieval(query, top_k=100)
for hit in hits:
    print(hit.rank, hit.score, hit.microbe)
```

Use S2M top-k as a candidate set, not as a reliable top-1 decision.

Metadata lookup:

```python
from r3_retrieval import lookup_metadata

row = lookup_metadata("P12345")
if row is not None:
    print(row["ec_number"], row["annotation"])
```

Known EC-4 gate:

```python
from r3_retrieval import is_known_ec4

if not is_known_ec4("99.99.99.99"):
    print("abstain due to unseen EC-4")
```

EC-3 fallback neighbors:

```python
from r3_retrieval import get_ec3_neighbors

neighbors = get_ec3_neighbors("1.14.13.99")
print(neighbors)
```

## Performance Summary

| Evidence | Metric | Status |
|---|---:|---|
| EC-4 grouped R2E validation | MRR about `0.918` | current R3 tool/verifier candidate |
| Leave-EC4-Out v2 cross-class EC-family transfer | HO EC-3 MRR `0.618702` | passes under teacher tolerance |
| Row-level identity retrieval | not a deployable open-domain claim | use only as corpus sanity check |
| E2M/S2M top-1 | about `0.006` | consume top-k as candidate sets |

## Agent v1 Gate

```python
from r3_retrieval import is_known_ec4, r2e_retrieval

hits = r2e_retrieval(reaction_emb, top_k=10)
top1 = hits[0] if hits else None

if top1 is None:
    decision = "abstain"
elif top1.score >= 0.9 and is_known_ec4(top1.ec_number):
    decision = "accept"
else:
    decision = "abstain"
```

For unseen EC-4 classes, use `get_ec3_neighbors()` to build a fallback set and
keep the final decision conservative.

## Open-Domain Reaction Query

The runtime package does not include torch, RDKit, DRFP generation, or model
checkpoint loading. Open-domain usage is:

```text
RxnSMILES -> DRFP externally -> r3_reaction_encoder.npz numpy forward
          -> L2-normalized reaction_emb -> r2e_retrieval(...)
```

See [`data/MODEL_ARCHITECTURE.md`](data/MODEL_ARCHITECTURE.md). The small
`data/r3_reaction_encoder.npz` file was exported from the frozen R3 checkpoint
and passed the row-0 `cosine >= 0.9999` sanity check with cosine `1.00000000`.

## Examples

```bash
python examples/01_r2e_basic.py --output_dir /path/to/r3/output
python examples/02_e2m_candidate_set.py --output_dir /path/to/r3/output
python examples/03_s2m_candidate_set.py --output_dir /path/to/r3/output
python examples/04_metadata_lookup.py --output_dir /path/to/r3/output
python examples/05_unseen_ec4_abstain.py --output_dir /path/to/r3/output
python examples/06_ec_classification.py --output_dir /path/to/r3/output
```

## Tests

```bash
pytest tests/ -v
```

The committed unit tests use small temporary fixtures so the GitHub repository
stays lightweight. Full R3 integration checks require the HPC artifacts listed
in `data/README.md`.

RULE-6 was also run on the real R3 HPC artifacts with
`R3_ARTIFACT_DIR=/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15`;
the result was `10 passed in 7.14s`.
