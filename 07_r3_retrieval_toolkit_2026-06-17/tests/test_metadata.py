import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval.loader import load_artifacts
from r3_retrieval.metadata import get_ec3_neighbors, is_known_ec4, lookup_metadata, normalize_metadata
from test_loader import make_artifact_dir


def test_lookup_metadata_hit_and_miss(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))

    hit = lookup_metadata("P00001", artifacts=art)
    miss = lookup_metadata("NO_SUCH_UNIPROT", artifacts=art)

    assert hit is not None
    assert hit["ec_number"] == "1.14.13.1"
    assert hit["annotation"] == "Example monooxygenase"
    assert miss is None


def test_unseen_ec4_returns_false(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))

    assert is_known_ec4("1.14.13.1", artifacts=art) is True
    assert is_known_ec4("99.99.99.99", artifacts=art) is False


def test_get_ec3_neighbors(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))

    assert get_ec3_neighbors("1.14.13.99", artifacts=art) == ["1.14.13.1", "1.14.13.2"]


def test_empty_metadata_fields_fallback_to_unknown():
    row = normalize_metadata(
        {
            "uniprot_id": "P00004",
            "ec_number": "3.1.1.1",
            "organism": "",
            "organism_taxonomy": "",
            "annotation": "",
            "assembly_accession": "",
        }
    )

    assert row["organism"] == "unknown"
    assert row["organism_taxonomy"] == "unknown"
    assert row["annotation"] == "unknown"
    assert row["assembly_accession"] == "unknown"
