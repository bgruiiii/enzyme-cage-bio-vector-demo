# R3 Toolkit Data Files

This directory is the local data mount point for the R3 retrieval toolkit.

Large R3 artifacts are intentionally not uploaded to GitHub:

- `embeddings_v3.npz` is large. The verified R3 HPC file is `568.78 MiB`.
- `metadata_v3.json` is large. The verified R3 HPC file is `21.66 MiB`.
- Full checkpoints such as `model_v3.pt` are not uploaded.

## Large File Download (NJU Box)

The two required large runtime artifacts are distributed through NJU Box
instead of GitHub.

| File | Size | SHA256 | Download link | Password | Expires |
|---|---:|---|---|---|---|
| `embeddings_v3.npz` | 568.78 MiB | `07418be8e79b7e9ae1dcb1bfdefd5cdacff87e4bc37e750c5918e6f5f73b8c14` | https://box.nju.edu.cn/f/a4994c6f51614603be50/ | (none) | permanent |
| `metadata_v3.json` | 21.66 MiB | `c1b02b21bef6ec759b81cb00fc9544a5e8acd00aea0a234cc15516dc9cd55ff1` | https://box.nju.edu.cn/f/cb833b2ad3a24ec69007/ | (none) | permanent |

The shared folder containing both files is:

```text
https://box.nju.edu.cn/d/f8cff4232a6f45dfac56/
```

The uploaded file names and byte sizes were checked against the HPC audit:

```text
embeddings_v3.npz  596407282 bytes
metadata_v3.json    22711862 bytes
```

Final R3 HPC output directory:

```text
/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/
```

To run the examples against the real R3 corpus, either copy these two files into
this `data/` directory or pass `--output_dir` to the examples:

```text
embeddings_v3.npz
metadata_v3.json
```

Example without copying large files:

```bash
python examples/01_r2e_basic.py \
  --output_dir /public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15
```

Expected real R3 artifact shape:

```text
reaction  (145607, 256) float32
enzyme    (145607, 256) float32
substrate (145607, 256) float32
microbe   (145607, 256) float32
metadata  145607 rows
```

`embeddings_v3.npz` contains these keys:

```text
reaction
enzyme
substrate
microbe
```

`metadata_v3.json` has schema `list[dict]` with 145607 rows. The observed
field union is:

```text
assembly_accession
ec_number
example_id
uniprot_id
```

The metadata file does not store RxnSMILES inline. For the v0.2 open-domain
sanity test only, row-0 RxnSMILES is resolved from the training feature file
`reaction_features.npz` by matching `example_id` and reading `cano_rxn_smiles`.

`r3_reaction_encoder.npz` is the small open-domain reaction encoder export. It
was generated from the frozen R3 checkpoint during RULE-11 and is included in
this directory.

```text
r3_reaction_encoder.npz
size: 5.6M
sha256: 1857a179f255130e3b561c76f8c752b93e58c423cc5c7e3187e9fa34db0b1e5c
row-0 numpy-forward cosine: 1.00000000
threshold: >= 0.9999
```
