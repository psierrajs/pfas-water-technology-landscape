from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path


RELEVANCE_LABELS = [
    "water_treatment",
    "adjacent_matrix",
    "treatment_unspecified_matrix",
    "contextual",
    "likely_irrelevant",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read relevance-classified records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def group_by_relevance(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group records by relevance label."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        label = row.get("relevance_label", "").strip()

        if label:
            grouped[label].append(row)

    return grouped


def build_sample(
    grouped: dict[str, list[dict[str, str]]],
    per_label: int,
    seed: int,
) -> list[dict[str, str]]:
    """Create a deterministic stratified relevance sample."""
    random_generator = random.Random(seed)
    sample = []

    for label in RELEVANCE_LABELS:
        candidates = grouped.get(label, [])
        sample_size = min(per_label, len(candidates))

        selected = random_generator.sample(
            candidates,
            sample_size,
        )

        for row in selected:
            sample.append(
                {
                    "sample_relevance_label": label,
                    "openalex_id": row.get("openalex_id", ""),
                    "doi": row.get("doi", ""),
                    "title": row.get("title", ""),
                    "abstract": row.get("abstract", ""),
                    "publication_year": row.get(
                        "publication_year",
                        "",
                    ),
                    "technology_labels": row.get(
                        "technology_labels",
                        "",
                    ),
                    "relevance_signals": row.get(
                        "relevance_signals",
                        "",
                    ),
                    "manual_relevance_label": "",
                    "manual_include": "",
                    "manual_notes": "",
                }
            )

    return sample


def write_csv(
    rows: list[dict[str, str]],
    output_path: Path,
) -> None:
    """Write the manual-review sample."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "sample_relevance_label",
        "openalex_id",
        "doi",
        "title",
        "abstract",
        "publication_year",
        "technology_labels",
        "relevance_signals",
        "manual_relevance_label",
        "manual_include",
        "manual_notes",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a stratified sample for relevance validation."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/processed/openalex_relevance_classified.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/processed/relevance_validation_sample.csv"
        ),
    )
    parser.add_argument(
        "--per-label",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.per_label < 1:
        raise ValueError("--per-label must be at least 1")

    rows = read_csv(args.input)
    grouped = group_by_relevance(rows)

    sample = build_sample(
        grouped,
        args.per_label,
        args.seed,
    )

    write_csv(sample, args.output)

    print(f"Relevance labels sampled: {len(grouped)}")
    print(f"Validation records written: {len(sample)}")
    print(f"Saved to: {args.output}")

    for label in RELEVANCE_LABELS:
        print(
            f"{label}: "
            f"{sum(
                row['sample_relevance_label'] == label
                for row in sample
            )}"
        )


if __name__ == "__main__":
    main()
