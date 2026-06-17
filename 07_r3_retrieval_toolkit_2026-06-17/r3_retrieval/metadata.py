"""Metadata lookup and EC helper APIs."""

from __future__ import annotations

from typing import Any

from .loader import get_default_artifacts


_INDEX_CACHE_BY_METADATA_ID: dict[int, dict[str, Any]] = {}


def _field(row: dict[str, Any], aliases: tuple[str, ...], default: Any = None) -> Any:
    for key in aliases:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return default


def canonical_uniprot(row: dict[str, Any]) -> str:
    return str(_field(row, ("uniprot_id", "UniprotID", "uniprot", "uid", "enzyme_id"), "unknown"))


def canonical_ec4(row: dict[str, Any]) -> str:
    return str(_field(row, ("ec_number", "EC number", "ec", "ec_number_raw"), "unknown"))


def canonical_microbe(row: dict[str, Any]) -> str:
    return str(_field(row, ("microbe", "microbe_name", "organism", "organism_name"), "unknown"))


def canonical_assembly(row: dict[str, Any]) -> str:
    return str(_field(row, ("assembly_accession", "assembly", "genome_accession"), "unknown"))


def ec3_of(ec_str: str) -> str:
    parts = str(ec_str).split(".")
    if len(parts) < 3:
        return str(ec_str)
    return ".".join(parts[:3])


def normalize_metadata(row: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with canonical keys added for downstream callers."""
    normalized = dict(row)
    normalized["uniprot_id"] = _field(normalized, ("uniprot_id",), canonical_uniprot(row))
    normalized["ec_number"] = _field(normalized, ("ec_number",), canonical_ec4(row))
    normalized["organism"] = _field(normalized, ("organism", "organism_name", "species"), "unknown")
    normalized["organism_taxonomy"] = _field(
        normalized,
        ("organism_taxonomy", "taxonomy", "lineage"),
        "unknown",
    )
    normalized["annotation"] = _field(
        normalized,
        ("annotation", "function", "protein_name", "description"),
        "unknown",
    )
    normalized["assembly_accession"] = _field(normalized, ("assembly_accession",), canonical_assembly(row))
    return normalized


def build_ec_index(metadata: list[dict[str, Any]]) -> dict[str, Any]:
    """Build one-pass EC and UniProt indexes from metadata rows."""
    ec4_set: set[str] = set()
    ec3_to_ec4s: dict[str, set[str]] = {}
    uniprot_to_row_index: dict[str, int] = {}

    for i, row in enumerate(metadata):
        ec4 = canonical_ec4(row)
        if ec4 and ec4 != "unknown":
            ec4_set.add(ec4)
            ec3_to_ec4s.setdefault(ec3_of(ec4), set()).add(ec4)

        uniprot = canonical_uniprot(row)
        if uniprot and uniprot != "unknown" and uniprot not in uniprot_to_row_index:
            uniprot_to_row_index[uniprot] = i

    return {
        "ec4_set": ec4_set,
        "ec3_to_ec4s": ec3_to_ec4s,
        "uniprot_to_row_index": uniprot_to_row_index,
    }


def get_ec_index(artifacts: dict[str, Any] | None = None) -> dict[str, Any]:
    artifacts = artifacts or get_default_artifacts()
    metadata = artifacts["metadata"]
    cache_key = id(metadata)
    if cache_key not in _INDEX_CACHE_BY_METADATA_ID:
        _INDEX_CACHE_BY_METADATA_ID[cache_key] = build_ec_index(metadata)
    return _INDEX_CACHE_BY_METADATA_ID[cache_key]


def lookup_metadata(uniprot_id: str, artifacts: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Return metadata for a UniProt ID, or None when it is absent."""
    artifacts = artifacts or get_default_artifacts()
    index = get_ec_index(artifacts)
    row_index = index["uniprot_to_row_index"].get(uniprot_id)
    if row_index is None:
        return None
    return normalize_metadata(artifacts["metadata"][row_index])


def is_known_ec4(ec_str: str, artifacts: dict[str, Any] | None = None) -> bool:
    """Return True when an EC-4 class appears in the R3 training metadata."""
    artifacts = artifacts or get_default_artifacts()
    return str(ec_str) in get_ec_index(artifacts)["ec4_set"]


def get_ec3_neighbors(ec_str: str, artifacts: dict[str, Any] | None = None) -> list[str]:
    """Return sorted training EC-4 classes that share the query EC-3 prefix."""
    artifacts = artifacts or get_default_artifacts()
    ec3 = ec3_of(ec_str)
    return sorted(get_ec_index(artifacts)["ec3_to_ec4s"].get(ec3, set()))
