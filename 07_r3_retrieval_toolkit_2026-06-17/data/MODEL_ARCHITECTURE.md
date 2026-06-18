# R3 Reaction Encoder Architecture

This file documents the numpy-forward contract for open-domain reaction queries.
Runtime retrieval stays pure numpy. Torch is only a build-time export dependency
for reading the frozen R3 checkpoint.

## Source Model

```text
Frozen checkpoint:
/public/home/acfbwjsi7s/bio_vector_full_run_2026-06-04/outputs/r3_ec4_balanced_stage3skip_2026-06-15/frozen/model_v3.pt

SHA256:
f728455ecc9d12c1eb3fc084fdc5445933befa5b7eb56a3644965fb4e0519c4c
```

## Reaction Encoder

```yaml
reaction_encoder:
  input:
    name: DRFP fingerprint
    shape: [2048]
    dtype: float32
  layers:
    - name: reaction_projector.net.0
      type: linear
      in: 2048
      out: 512
      bias: true
      activation: null
    - name: reaction_projector.net.1
      type: batchnorm1d
      features: 512
      mode: eval
      eps: 0.00001
      affine: true
    - name: reaction_projector.net.2
      type: relu
    - name: reaction_projector.net.3
      type: linear
      in: 512
      out: 512
      bias: true
      activation: null
    - name: reaction_projector.net.4
      type: batchnorm1d
      features: 512
      mode: eval
      eps: 0.00001
      affine: true
    - name: reaction_projector.net.5
      type: relu
    - name: reaction_projector.net.6
      type: linear
      in: 512
      out: 256
      bias: true
      activation: null
  output:
    name: reaction embedding
    shape: [256]
    post_processing: L2-normalize
  weights_file: r3_reaction_encoder.npz
  weights_layout:
    linear0_weight: [512, 2048]
    linear0_bias: [512]
    bn1_weight: [512]
    bn1_bias: [512]
    bn1_running_mean: [512]
    bn1_running_var: [512]
    linear3_weight: [512, 512]
    linear3_bias: [512]
    bn4_weight: [512]
    bn4_bias: [512]
    bn4_running_mean: [512]
    bn4_running_var: [512]
    linear6_weight: [256, 512]
    linear6_bias: [256]
```

## Numpy Forward Contract

For a batch `x` with shape `[batch, 2048]`:

```python
h = x @ linear0_weight.T + linear0_bias
h = (h - bn1_running_mean) / sqrt(bn1_running_var + eps) * bn1_weight + bn1_bias
h = maximum(h, 0)
h = h @ linear3_weight.T + linear3_bias
h = (h - bn4_running_mean) / sqrt(bn4_running_var + eps) * bn4_weight + bn4_bias
h = maximum(h, 0)
h = h @ linear6_weight.T + linear6_bias
reaction_emb = h / maximum(norm(h, axis=-1, keepdims=True), 1e-12)
```

## Required Export Sanity Check

After `r3_reaction_encoder.npz` is exported from `model_v3.pt`, run a corpus row
through the numpy forward and compare against `embeddings_v3.npz["reaction"][0]`.

Acceptance threshold:

```text
cosine(numpy_forward(drfp_row_0), embeddings_v3.npz["reaction"][0]) >= 0.9999
```

If the cosine is below `0.9999`, do not upload the export. Re-check the
state_dict keys, BatchNorm eval statistics, epsilon, and layer order.

## Substrate Encoder

The substrate projector uses the same layer pattern as the reaction projector
with input shape `[2048]` and output shape `[256]`, but it is a separate
state_dict branch (`substrate_projector.*`).

V1.5 exports this branch as:

```text
substrate_encoder_v3.npz
sha256: 0ba789a274674de5a1094c99421e86206041aa0bb111bdd912a9beb2e60a56cb
```

The substrate input is the training RDKit Morgan fingerprint:

```text
API: rdkit.Chem.AllChem.GetMorganFingerprintAsBitVect
radius: 2
nBits: 2048
useChirality: False
useFeatures: False
useBondTypes: True
```

The V1.5 row-0 sanity check compares the numpy-forward substrate embedding
against `embeddings_v3.npz["substrate"][0]` and passes with cosine
`1.0000000000`.
