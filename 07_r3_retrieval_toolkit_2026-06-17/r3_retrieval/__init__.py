"""Pure numpy R3 retrieval toolkit."""

from .loader import get_default_artifacts, load_artifacts, set_default_artifacts
from .metadata import build_ec_index, get_ec3_neighbors, is_known_ec4, lookup_metadata
from .retrieval import Candidate, MicrobeCandidate, e2m_retrieval, r2e_retrieval, s2m_retrieval
from .version import __version__

__all__ = [
    "__version__",
    "load_artifacts",
    "set_default_artifacts",
    "get_default_artifacts",
    "Candidate",
    "MicrobeCandidate",
    "r2e_retrieval",
    "e2m_retrieval",
    "s2m_retrieval",
    "lookup_metadata",
    "is_known_ec4",
    "get_ec3_neighbors",
    "build_ec_index",
]
