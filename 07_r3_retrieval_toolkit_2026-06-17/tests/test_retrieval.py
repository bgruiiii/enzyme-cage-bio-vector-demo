import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval.retrieval import Candidate, MicrobeCandidate, e2m_retrieval, r2e_retrieval, s2m_retrieval
from test_loader import make_artifact_dir
from r3_retrieval.loader import load_artifacts


def test_r2e_self_query_top1_score_high(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))
    hits = r2e_retrieval(art["reaction_emb"][0], top_k=3, artifacts=art)

    assert hits[0].row_index == 0
    assert hits[0].score > 0.99
    assert hits[0].rank == 1
    assert [hit.score for hit in hits] == sorted((hit.score for hit in hits), reverse=True)


def test_r2e_returns_dataclass_with_metadata(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))
    hits = r2e_retrieval(art["reaction_emb"][0], top_k=2, artifacts=art)

    assert isinstance(hits[0], Candidate)
    assert hits[0].organism != ""
    assert hits[0].annotation != ""
    assert hits[0].uniprot_id == "P00001"


def test_r2e_exclusion_controls(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))

    no_self = r2e_retrieval(art["reaction_emb"][0], top_k=2, artifacts=art, exclude_self_row_index=0)
    assert no_self[0].row_index == 1

    no_ec4 = r2e_retrieval(art["reaction_emb"][0], top_k=3, artifacts=art, exclude_ec4_set={"1.14.13.1"})
    assert all(hit.ec_number != "1.14.13.1" for hit in no_ec4)


def test_e2m_and_s2m_return_candidate_sets(tmp_path):
    art = load_artifacts(make_artifact_dir(tmp_path))

    e_hits = e2m_retrieval("P00001", top_k=2, artifacts=art)
    s_hits = s2m_retrieval(np.array([0, 1, 0, 0], dtype=np.float32), top_k=2, artifacts=art)

    assert len(e_hits) == 2
    assert len(s_hits) == 2
    assert isinstance(e_hits[0], MicrobeCandidate)
    assert e_hits[0].rank == 1
