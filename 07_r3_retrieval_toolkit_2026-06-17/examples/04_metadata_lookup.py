#!/usr/bin/env python3
"""Metadata lookup example."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import load_artifacts, lookup_metadata


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

    uniprot_id = art["metadata"][0].get("uniprot_id") or art["metadata"][0].get("UniprotID")
    if not uniprot_id:
        print("lookup_uniprot=None")
        print(None)
        return 0
    row = lookup_metadata(uniprot_id, artifacts=art)
    print(f"lookup_uniprot={uniprot_id}")
    print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
