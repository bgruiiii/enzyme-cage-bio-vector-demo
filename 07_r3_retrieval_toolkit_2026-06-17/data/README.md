# R3 Toolkit Data Files

This directory is the local data mount point for the R3 retrieval toolkit.

Large R3 artifacts are intentionally not uploaded to GitHub:

- `embeddings_v3.npz` is large. The verified R3 HPC file is `569M`.
- `metadata_v3.json` is large. The verified R3 HPC file is `22M`.
- Full checkpoints such as `model_v3.pt` are not uploaded.

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
