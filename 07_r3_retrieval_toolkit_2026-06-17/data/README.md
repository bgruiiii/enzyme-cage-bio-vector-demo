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

## V1.5 Substrate Open-Domain Assets

`substrate_encoder_v3.npz` is the small open-domain substrate encoder export. It
was generated from the frozen R3 checkpoint `substrate_projector.*` branch and
is included in this directory.

```text
substrate_encoder_v3.npz
size: 5.6M
size_bytes: 5794224
sha256: 0ba789a274674de5a1094c99421e86206041aa0bb111bdd912a9beb2e60a56cb
NJU Box: https://box.nju.edu.cn/f/e041cdc720b24299bfd0/
row-0 substrate numpy-forward cosine: 1.0000000000
threshold: >= 0.9999
```

The substrate input featurizer is the training RDKit Morgan fingerprint path:

```text
function: morgan_fp
API: rdkit.Chem.AllChem.GetMorganFingerprintAsBitVect
radius: 2
nBits: 2048
useChirality: False
useFeatures: False
useBondTypes: True
useCounts: False
output: 2048-d float32 bit vector
```

The row-0 substrate sanity check resolves metadata row-0
`example_id=TR000001_RHEA10012_P08159` through `reaction_features.npz`
`cano_rxn_smiles` and uses the reaction left side:

```text
CN1CCC[C@@H]1c1ccc(O)nc1.O.O=O
```

`reaction_features.npz` remains outside GitHub and is distributed through NJU
Box for BioDeg-side `example_id -> cano_rxn_smiles` lookup.

```text
reaction_features.npz
size: 16M
size_bytes: 16691154
sha256: c13d056ca28c3c243ea7884a4f50480779e26058f6d585c60fc057aa1f5ad917
NJU Box: https://box.nju.edu.cn/f/bb21eceb19e947dca534/
folder: https://box.nju.edu.cn/d/825d7f0611fb44afa451/
```

`reaction_features.npz` keys, shapes, and dtypes:

| Key | Shape | Dtype |
|---|---:|---|
| `cano_rxn_smiles` | `(145607,)` | `object` |
| `drfp` | `(145607, 2048)` | `float32` |
| `example_id` | `(145607,)` | `object` |
| `product_reacting_center_indices` | `(145607,)` | `object` |
| `rhea_id` | `(145607,)` | `int64` |
| `substrate_reacting_center_indices` | `(145607,)` | `object` |
| `uniprot_id` | `(145607,)` | `object` |
