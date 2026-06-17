"""Artifact loading for the R3 retrieval toolkit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np


_DEFAULT_ARTIFACTS: dict[str, Any] | None = None


def l2_normalize(x: np.ndarray) -> np.ndarray:
    """Return a float32 L2-normalized copy of x along the last axis."""
    arr = np.asarray(x, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return (arr / norms).astype(np.float32, copy=False)


def _load_optional(npz: np.lib.npyio.NpzFile, key: str) -> np.ndarray | None:
    if key not in npz.files:
        return None
    return l2_normalize(npz[key])


def load_artifacts(output_dir: str | Path) -> dict[str, Any]:
    """Load R3 embeddings and metadata from an output directory.

    Expected files:
        embeddings_v3.npz with keys reaction, enzyme, substrate, microbe
        metadata_v3.json with one row per corpus item

    Returned embeddings are float32 and L2-normalized. The large files are not
    committed to GitHub; see data/README.md for the R3 HPC location.
    """
    output_dir = Path(output_dir)
    npz_path = output_dir / "embeddings_v3.npz"
    metadata_path = output_dir / "metadata_v3.json"

    if not npz_path.exists():
        raise FileNotFoundError(f"Missing embeddings file: {npz_path}")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata file: {metadata_path}")

    npz = np.load(npz_path)
    with metadata_path.open() as f:
        metadata = json.load(f)

    artifacts = {
        "reaction_emb": l2_normalize(npz["reaction"]),
        "enzyme_emb": l2_normalize(npz["enzyme"]),
        "substrate_emb": _load_optional(npz, "substrate"),
        "microbe_emb": _load_optional(npz, "microbe"),
        "metadata": metadata,
    }

    n_rows = len(metadata)
    for key in ("reaction_emb", "enzyme_emb", "substrate_emb", "microbe_emb"):
        arr = artifacts[key]
        if arr is not None and arr.shape[0] != n_rows:
            raise ValueError(f"{key} rows ({arr.shape[0]}) do not match metadata ({n_rows})")

    return artifacts


def set_default_artifacts(artifacts_or_output_dir: dict[str, Any] | str | Path) -> dict[str, Any]:
    """Set process-local default artifacts for the retrieval and metadata APIs."""
    global _DEFAULT_ARTIFACTS
    if isinstance(artifacts_or_output_dir, dict):
        _DEFAULT_ARTIFACTS = artifacts_or_output_dir
    else:
        _DEFAULT_ARTIFACTS = load_artifacts(artifacts_or_output_dir)
    return _DEFAULT_ARTIFACTS


def get_default_artifacts() -> dict[str, Any]:
    """Return default artifacts previously set with set_default_artifacts()."""
    if _DEFAULT_ARTIFACTS is None:
        raise RuntimeError(
            "R3 artifacts are not loaded. Call set_default_artifacts(output_dir) "
            "or pass artifacts=... to the API."
        )
    return _DEFAULT_ARTIFACTS
