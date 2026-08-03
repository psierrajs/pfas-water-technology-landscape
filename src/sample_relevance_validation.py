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
    """Read records from a CSV file."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def normalize_title(title: str) -> str:
    """Normalize a title for fallback record matching."""
    return " ".join(title.lower().split())


def record_key(row: dict[str, str]) -> str:
    """Return the best available stable identifier for a record."""
    doi = row.get("doi", "").strip().lower()

    if doi:
        return f"doi:{doi}"

    openalex_id = row.get("openalex_id", "").strip().lower()

    if openalex_id:
        return f"openalex:{openalex_id}"

    title = normalize_title(row.get("title", ""))

    if title:
        return f"title:{title}"

    return ""


def build_exclusion_keys(
    paths: list[Path],
) -> set[str]:
    """Collect record identifiers from previous validation files."""
    keys: set[str] = set()

    for path in paths:
        for row in read_csv(path):
            key = record_key(row)

            if key:
                keys.add(key)

    return keys


def exclude_records(
    rows: list[dict[str, str]],
    excluded_keys: set[str],
) -> tuple[list[dict[str, str]], int]:
    """Remove records found in earlier validation samples."""
    retained = []
    excluded_count = 0

    for row in rows:
        key = record_key(row)

        if key and key in excluded_keys:
            excluded_count += 1
        else:
            retained.append(row)

    return retained, excluded_count


def group_by_relevance(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group records by relevance label."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        label = row.get("relevance_label", "").strip()

        if label in RELEVANCE_LABELS:
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
    force: bool,
) -> None:
    """Write the manual-review sample safely."""
    if output_path.exists() and not force:
        raise FileExistsError(
            f"Output already exists: {output_path}. "
            "Use --force to overwrite it."
        )

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
        "--exclude",
        type=Path,
        action="append",
        default=[],
        help=(
            "CSV containing records to exclude. "
            "May be supplied more than once."
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.per_label < 1:
        raise ValueError("--per-label must be at least 1")

    rows = read_csv(args.input)
    exclusion_keys = build_exclusion_keys(args.exclude)

    eligible_rows, excluded_count = exclude_records(
        rows,
        exclusion_keys,
    )

    grouped = group_by_relevance(eligible_rows)

    sample = build_sample(
        grouped,
        args.per_label,
        args.seed,
    )

    write_csv(
        sample,
        args.output,
        args.force,
    )

    print(f"Input records: {len(rows)}")
    print(f"Excluded previous records: {excluded_count}")
    print(f"Eligible records: {len(eligible_rows)}")
    print(f"Relevance labels sampled: {len(grouped)}")
    print(f"Validation records written: {len(sample)}")
    print(f"Saved to: {args.output}")

    for label in RELEVANCE_LABELS:
        count = sum(
            row["sample_relevance_label"] == label
            for row in sample
        )
        available = len(grouped.get(label, []))

        print(
            f"{label}: {count} sampled "
            f"from {available} eligible"
        )


if __name__ == "__main__":
    main()
