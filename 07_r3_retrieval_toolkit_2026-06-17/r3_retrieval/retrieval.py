"""Pure numpy retrieval primitives for R3 embeddings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .loader import get_default_artifacts, l2_normalize
from .metadata import canonical_assembly, canonical_ec4, canonical_microbe, canonical_uniprot, normalize_metadata


@dataclass(frozen=True)
class Candidate:
    uniprot_id: str
    ec_number: str
    organism: str
    organism_taxonomy: str
    annotation: str
    score: float
    rank: int
    row_index: int


@dataclass(frozen=True)
class MicrobeCandidate:
    microbe: str
    assembly_accession: str
    score: float
    rank: int
    row_index: int


def _artifacts(artifacts: dict[str, Any] | None) -> dict[str, Any]:
    return artifacts if artifacts is not None else get_default_artifacts()


def _query_vector(query: np.ndarray, expected_dim: int, name: str) -> np.ndarray:
    arr = np.asarray(query, dtype=np.float32)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be a 1D vector, got shape {arr.shape}")
    if arr.shape[0] != expected_dim:
        raise ValueError(f"{name} dim {arr.shape[0]} does not match corpus dim {expected_dim}")
    return l2_normalize(arr)


def _top_indices(scores: np.ndarray, top_k: int) -> list[int]:
    if top_k <= 0:
        return []
    k = min(int(top_k), scores.shape[0])
    if k == 0:
        return []
    partial = np.argpartition(-scores, kth=k - 1)[:k]
    return partial[np.argsort(-scores[partial])].tolist()


def _candidate_from_row(row: dict[str, Any], score: float, rank: int, row_index: int) -> Candidate:
    meta = normalize_metadata(row)
    return Candidate(
        uniprot_id=str(meta.get("uniprot_id") or "unknown"),
        ec_number=str(meta.get("ec_number") or "unknown"),
        organism=str(meta.get("organism") or "unknown"),
        organism_taxonomy=str(meta.get("organism_taxonomy") or "unknown"),
        annotation=str(meta.get("annotation") or "unknown"),
        score=float(score),
        rank=rank,
        row_index=int(row_index),
    )


def _microbe_candidate_from_row(row: dict[str, Any], score: float, rank: int, row_index: int) -> MicrobeCandidate:
    return MicrobeCandidate(
        microbe=canonical_microbe(row),
        assembly_accession=canonical_assembly(row),
        score=float(score),
        rank=rank,
        row_index=int(row_index),
    )


def r2e_retrieval(
    reaction_drfp_or_embedding: np.ndarray,
    top_k: int = 10,
    artifacts: dict[str, Any] | None = None,
    exclude_self_row_index: int | None = None,
    exclude_ec4_set: set[str] | None = None,
) -> list[Candidate]:
    """Retrieve enzyme candidates from a reaction embedding.

    The runtime API is pure numpy and does not encode raw DRFP by itself. For
    open-domain queries, encode DRFP externally using data/r3_reaction_encoder.npz
    and pass the resulting L2-normalized reaction embedding here.
    """
    art = _artifacts(artifacts)
    enzyme_emb = art["enzyme_emb"]
    metadata = art["metadata"]
    query = _query_vector(reaction_drfp_or_embedding, enzyme_emb.shape[1], "reaction query")

    scores = enzyme_emb @ query
    scores = scores.astype(np.float32, copy=True)

    if exclude_self_row_index is not None and 0 <= exclude_self_row_index < scores.shape[0]:
        scores[exclude_self_row_index] = -np.inf

    if exclude_ec4_set:
        banned = set(exclude_ec4_set)
        for i, row in enumerate(metadata):
            if canonical_ec4(row) in banned:
                scores[i] = -np.inf

    result = []
    for rank, row_index in enumerate(_top_indices(scores, top_k), start=1):
        if np.isneginf(scores[row_index]):
            continue
        result.append(_candidate_from_row(metadata[row_index], scores[row_index], rank, row_index))
    return result


def e2m_retrieval(
    enzyme_emb_or_uniprot: np.ndarray | str,
    top_k: int = 50,
    artifacts: dict[str, Any] | None = None,
) -> list[MicrobeCandidate]:
    """Retrieve microbe candidates from an enzyme embedding or UniProt ID.

    Do not consume top-1 as a reliable decision. The observed top-1 is about
    0.006; consume top_k as a candidate set for downstream filtering.
    """
    art = _artifacts(artifacts)
    enzyme_emb = art["enzyme_emb"]
    microbe_emb = art["microbe_emb"]
    metadata = art["metadata"]
    if microbe_emb is None:
        raise ValueError("microbe embeddings are absent from artifacts")

    if isinstance(enzyme_emb_or_uniprot, str):
        matches = [i for i, row in enumerate(metadata) if canonical_uniprot(row) == enzyme_emb_or_uniprot]
        if not matches:
            return []
        query = enzyme_emb[matches[0]]
    else:
        query = _query_vector(enzyme_emb_or_uniprot, microbe_emb.shape[1], "enzyme query")

    scores = microbe_emb @ l2_normalize(query)
    return [
        _microbe_candidate_from_row(metadata[row_index], scores[row_index], rank, row_index)
        for rank, row_index in enumerate(_top_indices(scores, top_k), start=1)
    ]


def s2m_retrieval(
    substrate_drfp_or_embedding: np.ndarray,
    top_k: int = 100,
    artifacts: dict[str, Any] | None = None,
) -> list[MicrobeCandidate]:
    """Retrieve microbe candidates from a substrate embedding.

    Do not consume top-1 as a reliable decision. The observed top-1 is about
    0.006; consume top_k as a candidate set for downstream filtering.
    """
    art = _artifacts(artifacts)
    microbe_emb = art["microbe_emb"]
    metadata = art["metadata"]
    if microbe_emb is None:
        raise ValueError("microbe embeddings are absent from artifacts")

    query = _query_vector(substrate_drfp_or_embedding, microbe_emb.shape[1], "substrate query")
    scores = microbe_emb @ query
    return [
        _microbe_candidate_from_row(metadata[row_index], scores[row_index], rank, row_index)
        for rank, row_index in enumerate(_top_indices(scores, top_k), start=1)
    ]
