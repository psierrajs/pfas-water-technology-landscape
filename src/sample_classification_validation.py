from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read classified OpenAlex records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def group_by_label(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group records by assigned technology label."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        labels = row.get("technology_labels", "").split(";")

        for label in labels:
            label = label.strip()

            if label:
                grouped[label].append(row)

    return grouped


def write_sample(
    rows: list[dict[str, str]],
    output_path: Path,
) -> None:
    """Write a human-review sample to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_label",
        "openalex_id",
        "doi",
        "title",
        "abstract",
        "publication_year",
        "source",
        "technology_labels",
        "manual_relevant",
        "manual_correct_labels",
        "manual_notes",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a stratified sample for classifier validation."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/openalex_classified.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/processed/classification_validation_sample.csv"
        ),
    )
    parser.add_argument(
        "--per-label",
        type=int,
        default=5,
        help="Number of records sampled for each technology label.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.per_label < 1:
        raise ValueError("--per-label must be at least 1")

    rows = read_csv(args.input)
    grouped = group_by_label(rows)
    random_generator = random.Random(args.seed)

    sample = []

    for label in sorted(grouped):
        candidates = grouped[label]
        sample_size = min(args.per_label, len(candidates))

        selected = random_generator.sample(
            candidates,
            sample_size,
        )

        for row in selected:
            sample.append(
                {
                    "sample_label": label,
                    "openalex_id": row.get("openalex_id", ""),
                    "doi": row.get("doi", ""),
                    "title": row.get("title", ""),
                    "abstract": row.get("abstract", ""),
                    "publication_year": row.get(
                        "publication_year",
                        "",
                    ),
                    "source": row.get("source", ""),
                    "technology_labels": row.get(
                        "technology_labels",
                        "",
                    ),
                    "manual_relevant": "",
                    "manual_correct_labels": "",
                    "manual_notes": "",
                }
            )

    write_sample(sample, args.output)

    print(f"Technology labels sampled: {len(grouped)}")
    print(f"Validation records written: {len(sample)}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
