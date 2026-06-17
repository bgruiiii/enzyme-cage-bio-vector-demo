#!/usr/bin/env python3
"""Unseen EC-4 abstain example."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import is_known_ec4, load_artifacts


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

    ec4 = "99.99.99.99"
    if not is_known_ec4(ec4, artifacts=art):
        print("abstain due to unseen EC-4")
    else:
        print("known EC-4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
