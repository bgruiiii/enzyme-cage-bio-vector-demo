import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
OPEN_DOMAIN_EXAMPLE = TOOLKIT_ROOT / "examples" / "00_drfp_open_domain_query.py"
RXN_SMILES_FIELDS = (
    "reaction_smiles",
    "rxn_smiles",
    "CANO_RXN_SMILES",
    "reaction",
    "rxn",
    "smiles",
)


def _load_open_domain_example():
    spec = importlib.util.spec_from_file_location("open_domain_query", OPEN_DOMAIN_EXAMPLE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _l2_normalize(x: np.ndarray) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float32)
    norm = np.linalg.norm(arr, axis=-1, keepdims=True)
    norm = np.maximum(norm, np.float32(1e-12))
    return (arr / norm).astype(np.float32, copy=False)


def _row0(metadata):
    if isinstance(metadata, list):
        if not metadata:
            raise AssertionError("metadata_v3.json is an empty list")
        return metadata[0]
    raise AssertionError(f"metadata_v3.json must be list[dict], got {type(metadata).__name__}")


def _reaction_smiles_from_row(row: dict) -> Optional[str]:
    for field in RXN_SMILES_FIELDS:
        value = row.get(field)
        if isinstance(value, str) and value:
            return value
    return None


def _reaction_smiles_from_features(row: dict) -> str:
    features_path = os.environ.get("REACTION_FEATURES_NPZ")
    if not features_path:
        raise AssertionError(
            "metadata row 0 has no recognized reaction smiles field and "
            "REACTION_FEATURES_NPZ is not set; "
            f"available metadata fields: {sorted(row.keys())}"
        )
    example_id = row.get("example_id")
    if not example_id:
        raise AssertionError(
            "metadata row 0 has no recognized reaction smiles field and no "
            "`example_id` for REACTION_FEATURES_NPZ lookup"
        )

    features = np.load(Path(features_path), allow_pickle=True)
    required = {"example_id", "cano_rxn_smiles"}
    missing = required.difference(features.files)
    if missing:
        raise AssertionError(f"REACTION_FEATURES_NPZ missing keys: {sorted(missing)}")

    example_ids = [str(x) for x in features["example_id"]]
    try:
        idx = example_ids.index(str(example_id))
    except ValueError as exc:
        raise AssertionError(f"example_id not found in REACTION_FEATURES_NPZ: {example_id}") from exc

    rxn_smiles = str(features["cano_rxn_smiles"][idx])
    if not rxn_smiles:
        raise AssertionError(f"empty cano_rxn_smiles for example_id: {example_id}")
    return rxn_smiles


def _reaction_smiles(row: dict) -> str:
    rxn_smiles = _reaction_smiles_from_row(row)
    if rxn_smiles is not None:
        return rxn_smiles
    return _reaction_smiles_from_features(row)


def test_open_domain_row0_reproduces_saved_reaction_embedding():
    output_dir = os.environ.get("R3_ARTIFACT_DIR")
    if not output_dir:
        pytest.skip("Set R3_ARTIFACT_DIR to run the real open-domain R3 sanity check")

    output_dir = Path(output_dir)
    metadata_path = output_dir / "metadata_v3.json"
    embeddings_path = output_dir / "embeddings_v3.npz"

    with metadata_path.open() as f:
        metadata = json.load(f)
    rxn_smiles = _reaction_smiles(_row0(metadata))

    module = _load_open_domain_example()
    pred = module.reaction_emb_open_domain(rxn_smiles)

    embeddings = np.load(embeddings_path)
    target = _l2_normalize(embeddings["reaction"][0:1])[0]
    cosine = float(np.dot(_l2_normalize(pred), target))

    print(f"open_domain_row0_cosine={cosine:.10f}")
    assert cosine >= 0.9999
