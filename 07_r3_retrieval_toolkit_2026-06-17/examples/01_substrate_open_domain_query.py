#!/usr/bin/env python3
"""Open-domain substrate SMILES to R3 substrate embedding example."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import load_artifacts, s2m_retrieval


TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENCODER_NPZ = TOOLKIT_ROOT / "data" / "substrate_encoder_v3.npz"

SUBSTRATE_FEATURIZER_NAME = "morgan_fp"
SUBSTRATE_MORGAN_RADIUS = 2
SUBSTRATE_MORGAN_N_BITS = 2048
SUBSTRATE_MORGAN_USE_CHIRALITY = False
SUBSTRATE_MORGAN_USE_FEATURES = False
SUBSTRATE_MORGAN_USE_BOND_TYPES = True
SUBSTRATE_MORGAN_USE_COUNTS = False

SUBSTRATE_SMILES_FIELDS = (
    "substrate_smiles",
    "canonical_substrate_smiles",
    "cano_substrate_smiles",
    "main_substrate_smiles",
)


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float32)
    norm = np.linalg.norm(arr, axis=-1, keepdims=True)
    norm = np.maximum(norm, np.float32(1e-12))
    return (arr / norm).astype(np.float32, copy=False)


def smiles_to_substrate_input(smiles: str) -> np.ndarray:
    """Training-compatible substrate SMILES -> 2048-bit Morgan input."""
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency rdkit. Install the training-compatible RDKit "
            "package before running open-domain substrate encoding."
        ) from exc

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.zeros(SUBSTRATE_MORGAN_N_BITS, dtype=np.float32)

    bit_info = None
    fp = AllChem.GetMorganFingerprintAsBitVect(
        mol,
        SUBSTRATE_MORGAN_RADIUS,
        nBits=SUBSTRATE_MORGAN_N_BITS,
        useChirality=SUBSTRATE_MORGAN_USE_CHIRALITY,
        useBondTypes=SUBSTRATE_MORGAN_USE_BOND_TYPES,
        useFeatures=SUBSTRATE_MORGAN_USE_FEATURES,
        bitInfo=bit_info,
    )
    arr = np.array(list(fp.ToBitString()), dtype=np.float32)
    if arr.shape != (SUBSTRATE_MORGAN_N_BITS,):
        raise ValueError(f"Expected Morgan shape ({SUBSTRATE_MORGAN_N_BITS},), got {arr.shape}")
    return arr


def _linear(x: np.ndarray, weight: np.ndarray, bias: np.ndarray) -> np.ndarray:
    return x @ weight.T + bias


def _batch_norm_eval(
    x: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray,
    running_mean: np.ndarray,
    running_var: np.ndarray,
    eps: np.ndarray,
) -> np.ndarray:
    return (x - running_mean) / np.sqrt(running_var + eps) * weight + bias


def substrate_emb_from_input(
    substrate_input: np.ndarray,
    encoder_npz: str | Path = DEFAULT_ENCODER_NPZ,
) -> np.ndarray:
    """Project a 2048-dim substrate Morgan vector into the frozen R3 space."""
    x = np.asarray(substrate_input, dtype=np.float32)
    if x.shape != (SUBSTRATE_MORGAN_N_BITS,):
        raise ValueError(f"Expected substrate input shape ({SUBSTRATE_MORGAN_N_BITS},), got {x.shape}")

    weights = np.load(Path(encoder_npz), allow_pickle=False)
    eps = np.asarray(weights["eps"] if "eps" in weights.files else 1e-5, dtype=np.float32)

    h = x.reshape(1, -1)
    h = _linear(h, weights["linear0_weight"], weights["linear0_bias"])
    h = _batch_norm_eval(
        h,
        weights["bn1_weight"],
        weights["bn1_bias"],
        weights["bn1_running_mean"],
        weights["bn1_running_var"],
        eps,
    )
    h = np.maximum(h, 0)
    h = _linear(h, weights["linear3_weight"], weights["linear3_bias"])
    h = _batch_norm_eval(
        h,
        weights["bn4_weight"],
        weights["bn4_bias"],
        weights["bn4_running_mean"],
        weights["bn4_running_var"],
        eps,
    )
    h = np.maximum(h, 0)
    h = _linear(h, weights["linear6_weight"], weights["linear6_bias"])
    return _l2_normalize(h)[0]


def smiles_to_substrate_emb(
    smiles: str,
    encoder_npz: str | Path = DEFAULT_ENCODER_NPZ,
) -> np.ndarray:
    """Complete SMILES -> 256-d substrate embedding path."""
    return substrate_emb_from_input(smiles_to_substrate_input(smiles), encoder_npz=encoder_npz)


def _row0(metadata):
    if isinstance(metadata, list):
        if not metadata:
            raise ValueError("metadata_v3.json is an empty list")
        return metadata[0]
    raise ValueError(f"metadata_v3.json must be list[dict], got {type(metadata).__name__}")


def _substrate_smiles_from_row(row: dict) -> Optional[str]:
    for field in SUBSTRATE_SMILES_FIELDS:
        value = row.get(field)
        if isinstance(value, str) and value:
            return value
    return None


def _substrate_smiles_from_reaction_features(row: dict, reaction_features_npz: str | Path | None) -> str:
    features_path = reaction_features_npz or os.environ.get("REACTION_FEATURES_NPZ")
    if not features_path:
        raise ValueError(
            "metadata row 0 has no recognized substrate smiles field and "
            "REACTION_FEATURES_NPZ was not provided"
        )

    example_id = row.get("example_id")
    if not example_id:
        raise ValueError("metadata row 0 has no `example_id` for reaction_features.npz lookup")

    features = np.load(Path(features_path), allow_pickle=True)
    required = {"example_id", "cano_rxn_smiles"}
    missing = required.difference(features.files)
    if missing:
        raise ValueError(f"reaction_features.npz missing keys: {sorted(missing)}")

    example_ids = [str(x) for x in features["example_id"]]
    try:
        idx = example_ids.index(str(example_id))
    except ValueError as exc:
        raise ValueError(f"example_id not found in reaction_features.npz: {example_id}") from exc

    rxn_smiles = str(features["cano_rxn_smiles"][idx])
    if ">>" not in rxn_smiles:
        raise ValueError(f"cano_rxn_smiles has no reaction separator for example_id: {example_id}")
    substrate_smiles = rxn_smiles.split(">>", 1)[0]
    if not substrate_smiles:
        raise ValueError(f"empty substrate side for example_id: {example_id}")
    return substrate_smiles


def _metadata_row0_substrate_smiles(row: dict, reaction_features_npz: str | Path | None = None) -> str:
    substrate_smiles = _substrate_smiles_from_row(row)
    if substrate_smiles is not None:
        return substrate_smiles
    return _substrate_smiles_from_reaction_features(row, reaction_features_npz)


def sanity_check(
    metadata_path: str | Path,
    substrate_corpus_npz: str | Path,
    encoder_npz: str | Path,
    reaction_features_npz: str | Path | None = None,
) -> dict:
    """Reproduce metadata row-0 substrate embedding and compare to corpus row 0."""
    with Path(metadata_path).open() as f:
        metadata = json.load(f)
    row = _row0(metadata)
    substrate_smiles = _metadata_row0_substrate_smiles(row, reaction_features_npz)

    pred = smiles_to_substrate_emb(substrate_smiles, encoder_npz=encoder_npz)
    corpus = np.load(Path(substrate_corpus_npz), allow_pickle=False)
    if "substrate" not in corpus.files:
        raise ValueError("substrate corpus npz must contain key `substrate`")
    target = _l2_normalize(corpus["substrate"][0:1])[0]
    cosine = float(np.dot(_l2_normalize(pred), target))
    return {
        "metadata_row0_example_id": row.get("example_id"),
        "metadata_row0_substrate_smiles": substrate_smiles,
        "substrate_input_shape": smiles_to_substrate_input(substrate_smiles).shape,
        "substrate_embedding_shape": pred.shape,
        "corpus_substrate_row0_shape": target.shape,
        "cosine_to_corpus_emb": cosine,
        "pass": cosine >= 0.9999,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smiles", default=None)
    parser.add_argument("--encoder_npz", default=str(DEFAULT_ENCODER_NPZ))
    parser.add_argument("--output_dir", default=None)
    parser.add_argument("--top_k", type=int, default=10)
    parser.add_argument("--metadata_path", default=None)
    parser.add_argument("--substrate_corpus_npz", default=None)
    parser.add_argument("--reaction_features_npz", default=None)
    parser.add_argument("--sanity", action="store_true")
    args = parser.parse_args()

    if args.sanity:
        if not args.metadata_path or not args.substrate_corpus_npz:
            print("--sanity requires --metadata_path and --substrate_corpus_npz")
            return 1
        result = sanity_check(
            args.metadata_path,
            args.substrate_corpus_npz,
            args.encoder_npz,
            reaction_features_npz=args.reaction_features_npz,
        )
        for key, value in result.items():
            print(f"{key}={value}")
        return 0 if result["pass"] else 1

    if not args.smiles:
        print("--smiles is required unless --sanity is set")
        return 1

    try:
        emb = smiles_to_substrate_emb(args.smiles, encoder_npz=args.encoder_npz)
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"Open-domain substrate encoding failed: {exc}")
        return 1

    print(f"substrate_featurizer={SUBSTRATE_FEATURIZER_NAME}")
    print(f"morgan_radius={SUBSTRATE_MORGAN_RADIUS}")
    print(f"morgan_n_bits={SUBSTRATE_MORGAN_N_BITS}")
    print(f"morgan_use_chirality={SUBSTRATE_MORGAN_USE_CHIRALITY}")
    print(f"morgan_use_features={SUBSTRATE_MORGAN_USE_FEATURES}")
    print(f"substrate_embedding_shape={emb.shape}")
    print(f"substrate_embedding_l2_norm={np.linalg.norm(emb):.8f}")

    if args.output_dir:
        try:
            art = load_artifacts(args.output_dir)
        except FileNotFoundError as exc:
            print(f"Missing R3 artifacts for retrieval: {exc}")
            return 1
        hits = s2m_retrieval(emb, top_k=args.top_k, artifacts=art)
        print(f"s2m_top_k={len(hits)}")
        for hit in hits:
            print(f"{hit.rank}\t{hit.score:.6f}\t{hit.assembly_accession}\t{hit.microbe}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
