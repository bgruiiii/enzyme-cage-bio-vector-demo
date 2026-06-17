#!/usr/bin/env python3
"""Basic R2E retrieval example."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from r3_retrieval import load_artifacts, r2e_retrieval


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

    hits = r2e_retrieval(art["reaction_emb"][0], top_k=5, artifacts=art)
    print("R2E top-5 for metadata row 0")
    for hit in hits:
        print(f"{hit.rank}\t{hit.score:.6f}\t{hit.uniprot_id}\t{hit.ec_number}\t{hit.annotation}")
    if hits:
        print(f"top1_score={hits[0].score:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
