#!/usr/bin/env python3
"""E2M candidate-set retrieval example."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import e2m_retrieval, load_artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", default=str(Path(__file__).resolve().parents[1] / "data"))
    args = parser.parse_args()

    try:
        art = load_artifacts(args.output_dir)
    except FileNotFoundError as exc:
        print(f"Missing R3 artifacts: {exc}")
        print("Copy embeddings_v3.npz and metadata_v3.json into data/ or pass --output_dir.")
        return 0

    print("WARNING: E2M top-1 is about 0.006; use top_k as a candidate set.")
    hits = e2m_retrieval(art["enzyme_emb"][0], top_k=50, artifacts=art)
    print(f"E2M candidates={len(hits)}")
    for hit in hits[:10]:
        print(f"{hit.rank}\t{hit.score:.6f}\t{hit.assembly_accession}\t{hit.microbe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
