#!/usr/bin/env python3
"""EC-4 classification by R2E top-k majority vote."""

import argparse
import sys
from collections import Counter
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

    hits = r2e_retrieval(art["reaction_emb"][0], top_k=10, artifacts=art)
    if not hits:
        print("predicted_ec4=None")
        print("top10_votes={}")
        print("abstain due to empty R2E result set")
        return 0
    votes = Counter(hit.ec_number for hit in hits)
    predicted, count = votes.most_common(1)[0]
    print(f"predicted_ec4={predicted}")
    print(f"top10_votes={dict(votes)}")
    print(f"winning_votes={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
