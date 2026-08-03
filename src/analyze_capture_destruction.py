from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


CAPTURE_TECHNOLOGIES = {
    "adsorption",
    "ion_exchange",
    "membranes",
}

DESTRUCTION_TECHNOLOGIES = {
    "photocatalysis",
    "electrochemical_oxidation",
    "plasma",
    "hydrothermal",
    "sonolysis",
    "biological",
    "thermal",
    "supercritical_water_oxidation",
}

EXPLICIT_COMBINED_LABEL = "capture_and_destroy"

ANALYSIS_GROUPS = [
    "capture_only",
    "destruction_only",
    "capture_and_destruction",
    "unclassified",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read the analysis-ready corpus."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_labels(value: str) -> set[str]:
    """Parse unique semicolon-delimited technology labels."""
    return {
        label.strip()
        for label in value.split(";")
        if label.strip()
    }


def parse_year(value: str) -> int | None:
    """Return a valid publication year."""
    try:
        year = int(value.strip())
    except ValueError:
        return None

    if 1900 <= year <= 2100:
        return year

    return None


def classify_strategy(labels: set[str]) -> str:
    """Assign a capture/destruction strategy group."""
    has_capture = bool(labels & CAPTURE_TECHNOLOGIES)
    has_destruction = bool(labels & DESTRUCTION_TECHNOLOGIES)
    has_explicit_combination = EXPLICIT_COMBINED_LABEL in labels

    if has_explicit_combination or (
        has_capture and has_destruction
    ):
        return "capture_and_destruction"

    if has_capture:
        return "capture_only"

    if has_destruction:
        return "destruction_only"

    return "unclassified"


def enrich_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Add strategy classifications to corpus records."""
    enriched_rows = []

    for row in rows:
        labels = parse_labels(
            row.get("technology_labels", "")
        )
        strategy = classify_strategy(labels)

        enriched = dict(row)
        enriched["treatment_strategy"] = strategy
        enriched["has_capture_technology"] = (
            "yes"
            if labels & CAPTURE_TECHNOLOGIES
            else "no"
        )
        enriched["has_destruction_technology"] = (
            "yes"
            if labels & DESTRUCTION_TECHNOLOGIES
            else "no"
        )
        enriched["has_explicit_combined_label"] = (
            "yes"
            if EXPLICIT_COMBINED_LABEL in labels
            else "no"
        )

        enriched_rows.append(enriched)

    return enriched_rows

def build_strategy_summary(
    rows: list[dict[str, Any]],
) -> list[dict[str, object]]:
    """Summarize records by treatment strategy."""
    counts = Counter(
        str(row["treatment_strategy"])
        for row in rows
    )

    total = len(rows)

    return [
        {
            "treatment_strategy": strategy,
            "record_count": counts[strategy],
            "percentage_of_corpus": (
                f"{counts[strategy] / total:.4f}"
                if total
                else "0.0000"
            ),
        }
        for strategy in ANALYSIS_GROUPS
    ]


def build_year_summary(
    rows: list[dict[str, Any]],
) -> list[dict[str, object]]:
    """Count strategies by publication year."""
    counts: Counter[tuple[int, str]] = Counter()

    for row in rows:
        year = parse_year(
            str(row.get("publication_year", ""))
        )

        if year is None:
            continue

        strategy = str(row["treatment_strategy"])
        counts[(year, strategy)] += 1

    return [
        {
            "publication_year": year,
            "treatment_strategy": strategy,
            "record_count": count,
        }
        for (year, strategy), count in sorted(counts.items())
    ]


def build_tier_summary(
    rows: list[dict[str, Any]],
) -> list[dict[str, object]]:
    """Count strategies within each analysis tier."""
    counts: Counter[tuple[str, str]] = Counter()

    for row in rows:
        tier = str(row.get("analysis_tier", "")).strip()
        strategy = str(row["treatment_strategy"])

        counts[(tier, strategy)] += 1

    return [
        {
            "analysis_tier": tier,
            "treatment_strategy": strategy,
            "record_count": count,
        }
        for (tier, strategy), count in sorted(counts.items())
    ]


def build_combination_summary(
    rows: list[dict[str, Any]],
) -> list[dict[str, object]]:
    """Count capture/destruction technology pairs."""
    pair_counts: Counter[tuple[str, str]] = Counter()

    for row in rows:
        labels = parse_labels(
            str(row.get("technology_labels", ""))
        )

        capture_labels = sorted(
            labels & CAPTURE_TECHNOLOGIES
        )
        destruction_labels = sorted(
            labels & DESTRUCTION_TECHNOLOGIES
        )

        for capture in capture_labels:
            for destruction in destruction_labels:
                pair_counts[(capture, destruction)] += 1

    return [
        {
            "capture_technology": capture,
            "destruction_technology": destruction,
            "record_count": count,
        }
        for (capture, destruction), count in sorted(
            pair_counts.items(),
            key=lambda item: (
                -item[1],
                item[0][0],
                item[0][1],
            ),
        )
    ]


def write_csv(
    rows: list[dict[str, object]],
    path: Path,
    fieldnames: list[str],
) -> None:
    """Write a summary CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    rows: list[dict[str, Any]],
    combination_summary: list[dict[str, object]],
) -> None:
    """Print high-level strategy findings."""
    counts = Counter(
        str(row["treatment_strategy"])
        for row in rows
    )

    print(f"Input records: {len(rows)}")

    print("\nTreatment strategies")
    print("-" * 40)

    for strategy in ANALYSIS_GROUPS:
        print(f"{strategy}: {counts[strategy]}")

    print("\nTop capture/destruction combinations")
    print("-" * 60)

    if not combination_summary:
        print("No combined technology records found")
        return

    for row in combination_summary[:15]:
        print(
            f"{row['capture_technology']} + "
            f"{row['destruction_technology']}: "
            f"{row['record_count']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare capture, destruction and combined PFAS "
            "treatment strategies."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/processed/openalex_analysis_corpus.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "data/processed/capture_destruction"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)

    if not rows:
        raise ValueError("The analysis corpus contains no records")

    enriched_rows = enrich_rows(rows)
    strategy_summary = build_strategy_summary(enriched_rows)
    year_summary = build_year_summary(enriched_rows)
    tier_summary = build_tier_summary(enriched_rows)
    combination_summary = build_combination_summary(
        enriched_rows
    )

    write_csv(
        strategy_summary,
        args.output_dir / "strategy_summary.csv",
        [
            "treatment_strategy",
            "record_count",
            "percentage_of_corpus",
        ],
    )
    write_csv(
        year_summary,
        args.output_dir / "strategy_by_year.csv",
        [
            "publication_year",
            "treatment_strategy",
            "record_count",
        ],
    )
    write_csv(
        tier_summary,
        args.output_dir / "strategy_by_tier.csv",
        [
            "analysis_tier",
            "treatment_strategy",
            "record_count",
        ],
    )
    write_csv(
        combination_summary,
        args.output_dir / "technology_combinations.csv",
        [
            "capture_technology",
            "destruction_technology",
            "record_count",
        ],
    )

    print_summary(enriched_rows, combination_summary)
    print(f"\nSaved outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()