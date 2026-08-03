from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


ANALYSIS_TIERS = {
    "water_treatment": "core",
    "adjacent_matrix": "secondary",
    "treatment_unspecified_matrix": "manual_review",
    "contextual": "background",
    "likely_irrelevant": "exclude_candidate",
}

INCLUSION_RECOMMENDATIONS = {
    "water_treatment": "include",
    "adjacent_matrix": "include",
    "treatment_unspecified_matrix": "review",
    "contextual": "selective",
    "likely_irrelevant": "exclude_candidate",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read relevance-classified OpenAlex records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def enrich_records(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Add operational analysis fields to every record."""
    enriched_rows = []

    for row in rows:
        relevance_label = row.get(
            "relevance_label",
            "",
        ).strip()

        if relevance_label not in ANALYSIS_TIERS:
            raise ValueError(
                f"Unknown relevance label: {relevance_label!r}"
            )

        enriched = dict(row)
        enriched["analysis_tier"] = ANALYSIS_TIERS[
            relevance_label
        ]
        enriched["inclusion_recommendation"] = (
            INCLUSION_RECOMMENDATIONS[relevance_label]
        )
        enriched["manual_screening_required"] = (
            "yes"
            if relevance_label
            == "treatment_unspecified_matrix"
            else "no"
        )

        enriched_rows.append(enriched)

    return enriched_rows


def write_csv(
    rows: list[dict[str, Any]],
    path: Path,
) -> None:
    """Write the analysis-ready corpus."""
    if not rows:
        raise ValueError("No records available to write")

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    rows: list[dict[str, Any]],
) -> None:
    """Print counts by analysis tier and recommendation."""
    tier_counts = Counter(
        str(row["analysis_tier"])
        for row in rows
    )
    recommendation_counts = Counter(
        str(row["inclusion_recommendation"])
        for row in rows
    )

    print(f"Input records: {len(rows)}")

    print("\nAnalysis tiers")
    print("-" * 40)

    for tier, count in sorted(tier_counts.items()):
        print(f"{tier}: {count}")

    print("\nInclusion recommendations")
    print("-" * 40)

    for recommendation, count in sorted(
        recommendation_counts.items()
    ):
        print(f"{recommendation}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create an analysis-ready PFAS literature corpus "
            "from relevance-classified OpenAlex records."
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
            "data/processed/openalex_analysis_corpus.csv"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    enriched_rows = enrich_records(rows)
    write_csv(enriched_rows, args.output)
    print_summary(enriched_rows)

    print(f"\nSaved to: {args.output}")


if __name__ == "__main__":
    main()
