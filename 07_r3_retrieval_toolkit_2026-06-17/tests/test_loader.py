import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval.loader import load_artifacts


def make_artifact_dir(tmp_path: Path) -> Path:
    metadata = [
        {
            "uniprot_id": "P00001",
            "ec_number": "1.14.13.1",
            "organism": "Escherichia coli",
            "organism_taxonomy": "Bacteria/Proteobacteria",
            "annotation": "Example monooxygenase",
            "assembly_accession": "GCF_000001",
        },
        {
            "uniprot_id": "P00002",
            "ec_number": "1.14.13.2",
            "organism": "Bacillus subtilis",
            "organism_taxonomy": "Bacteria/Firmicutes",
            "annotation": "Example oxidoreductase",
            "assembly_accession": "GCF_000002",
        },
        {
            "uniprot_id": "P00003",
            "ec_number": "2.7.1.1",
            "organism": "Saccharomyces cerevisiae",
            "organism_taxonomy": "Eukaryota/Fungi",
            "annotation": "Example kinase",
            "assembly_accession": "GCF_000003",
        },
    ]
    np.savez(
        tmp_path / "embeddings_v3.npz",
        reaction=np.array([[1, 0, 0, 0], [0.8, 0.2, 0, 0], [0, 0, 1, 0]], dtype=np.float32),
        enzyme=np.array([[1, 0, 0, 0], [0.8, 0.2, 0, 0], [0, 0, 1, 0]], dtype=np.float32),
        substrate=np.array([[0, 1, 0, 0], [0, 0.8, 0.2, 0], [0, 0, 0, 1]], dtype=np.float32),
        microbe=np.array([[0, 1, 0, 0], [0, 0.8, 0.2, 0], [0, 0, 0, 1]], dtype=np.float32),
    )
    (tmp_path / "metadata_v3.json").write_text(json.dumps(metadata), encoding="utf-8")
    return tmp_path


def test_load_artifacts(tmp_path):
    artifact_dir = make_artifact_dir(tmp_path)
    art = load_artifacts(artifact_dir)

    assert set(art) == {"reaction_emb", "enzyme_emb", "substrate_emb", "microbe_emb", "metadata"}
    assert art["reaction_emb"].shape == (3, 4)
    assert art["enzyme_emb"].dtype == np.float32
    assert len(art["metadata"]) == 3
    assert np.allclose(np.linalg.norm(art["reaction_emb"], axis=-1), 1.0, atol=1e-6)


def test_real_r3_artifacts_shape_when_available():
    output_dir = os.environ.get("R3_ARTIFACT_DIR")
    if not output_dir:
        pytest.skip("Set R3_ARTIFACT_DIR to run the real 145607-row R3 artifact check")

    art = load_artifacts(output_dir)

    assert art["reaction_emb"].shape[0] == 145607
    assert art["enzyme_emb"].shape[0] == 145607
    assert len(art["metadata"]) == 145607
    assert np.allclose(np.linalg.norm(art["reaction_emb"], axis=-1), 1.0, atol=1e-5)
