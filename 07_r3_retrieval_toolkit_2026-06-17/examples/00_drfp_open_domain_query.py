#!/usr/bin/env python3
"""Open-domain RxnSMILES to R3 reaction embedding example."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import load_artifacts, r2e_retrieval


TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENCODER_NPZ = TOOLKIT_ROOT / "data" / "r3_reaction_encoder.npz"

DRFP_LIBRARY_VERSION = "drfp==0.3.6"
DRFP_N_FOLDED_LENGTH = 2048
DRFP_TRAINING_CALL = "DrfpEncoder.encode([rxn_smiles]) with drfp==0.3.6 defaults"


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float32)
    norm = np.linalg.norm(arr, axis=-1, keepdims=True)
    norm = np.maximum(norm, np.float32(1e-12))
    return (arr / norm).astype(np.float32, copy=False)


def smiles_to_drfp(rxn_smiles: str) -> np.ndarray:
    """Encode one RxnSMILES string with the training DRFP dependency.

    The R3 feature builder used `drfp==0.3.6` and called
    `DrfpEncoder.encode([rxn])` without keyword overrides. Keep this function
    aligned with that call path; the row-0 cosine sanity test is the required
    proof that the DRFP parameters match the frozen R3 artifacts.
    """
    try:
        from drfp import DrfpEncoder
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency drfp. Install the training-compatible package "
            "`drfp==0.3.6` before running open-domain DRFP encoding."
        ) from exc

    encoded = DrfpEncoder.encode([rxn_smiles])
    drfp = np.asarray(encoded[0], dtype=np.float32)
    if drfp.shape != (DRFP_N_FOLDED_LENGTH,):
        raise ValueError(f"Expected DRFP shape ({DRFP_N_FOLDED_LENGTH},), got {drfp.shape}")
    return drfp


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


def reaction_emb_from_drfp(
    drfp: np.ndarray,
    encoder_npz: str | Path = DEFAULT_ENCODER_NPZ,
) -> np.ndarray:
    """Project a 2048-dim DRFP vector into the frozen R3 reaction space."""
    x = np.asarray(drfp, dtype=np.float32)
    if x.shape != (DRFP_N_FOLDED_LENGTH,):
        raise ValueError(f"Expected DRFP shape ({DRFP_N_FOLDED_LENGTH},), got {x.shape}")

    weights = np.load(Path(encoder_npz))
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


def reaction_emb_open_domain(
    rxn_smiles: str,
    encoder_npz: str | Path = DEFAULT_ENCODER_NPZ,
) -> np.ndarray:
    """Encode an open-domain RxnSMILES string into an R3 reaction embedding."""
    return reaction_emb_from_drfp(smiles_to_drfp(rxn_smiles), encoder_npz=encoder_npz)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rxn_smiles", required=True)
    parser.add_argument("--encoder_npz", default=str(DEFAULT_ENCODER_NPZ))
    parser.add_argument("--output_dir", default=None)
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    try:
        emb = reaction_emb_open_domain(args.rxn_smiles, encoder_npz=args.encoder_npz)
    except (RuntimeError, FileNotFoundError, ValueError) as exc:
        print(f"Open-domain encoding failed: {exc}")
        return 1

    print(f"drfp_dependency={DRFP_LIBRARY_VERSION}")
    print(f"drfp_training_call={DRFP_TRAINING_CALL}")
    print(f"reaction_embedding_shape={emb.shape}")
    print(f"reaction_embedding_l2_norm={np.linalg.norm(emb):.8f}")

    if args.output_dir:
        try:
            art = load_artifacts(args.output_dir)
        except FileNotFoundError as exc:
            print(f"Missing R3 artifacts for retrieval: {exc}")
            return 1
        hits = r2e_retrieval(emb, top_k=args.top_k, artifacts=art)
        print(f"r2e_top_k={len(hits)}")
        for hit in hits:
            print(f"{hit.rank}\t{hit.score:.6f}\t{hit.uniprot_id}\t{hit.ec_number}\t{hit.annotation}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
