from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


VALID_ANALYSIS_TIERS = {
    "core",
    "secondary",
    "manual_review",
    "background",
    "exclude_candidate",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read the analysis-ready OpenAlex corpus."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_year(value: str) -> int | None:
    """Return a valid four-digit publication year."""
    value = value.strip()

    if not value:
        return None

    try:
        year = int(value)
    except ValueError:
        return None

    if 1900 <= year <= 2100:
        return year

    return None


def parse_technology_labels(value: str) -> list[str]:
    """Split a semicolon-delimited technology-label field."""
    labels = []

    for label in value.split(";"):
        normalized = label.strip()

        if normalized and normalized not in labels:
            labels.append(normalized)

    return labels


def write_rows(
    rows: Iterable[dict[str, object]],
    path: Path,
    fieldnames: list[str],
) -> None:
    """Write analysis results to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def build_year_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Count publications by year."""
    counts: Counter[int] = Counter()

    for row in rows:
        year = parse_year(row.get("publication_year", ""))

        if year is not None:
            counts[year] += 1

    return [
        {
            "publication_year": year,
            "publication_count": counts[year],
        }
        for year in sorted(counts)
    ]


def build_year_tier_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Count publications by year and operational analysis tier."""
    counts: Counter[tuple[int, str]] = Counter()

    for row in rows:
        year = parse_year(row.get("publication_year", ""))
        tier = row.get("analysis_tier", "").strip()

        if year is None or tier not in VALID_ANALYSIS_TIERS:
            continue

        counts[(year, tier)] += 1

    return [
        {
            "publication_year": year,
            "analysis_tier": tier,
            "publication_count": count,
        }
        for (year, tier), count in sorted(counts.items())
    ]


def build_year_technology_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Count technology-labelled publications by year."""
    counts: Counter[tuple[int, str]] = Counter()

    for row in rows:
        year = parse_year(row.get("publication_year", ""))

        if year is None:
            continue

        labels = parse_technology_labels(
            row.get("technology_labels", "")
        )

        for label in labels:
            counts[(year, label)] += 1

    return [
        {
            "publication_year": year,
            "technology_label": label,
            "publication_count": count,
        }
        for (year, label), count in sorted(counts.items())
    ]


def build_technology_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Summarize total records and years for each technology."""
    counts: Counter[str] = Counter()
    years: dict[str, list[int]] = defaultdict(list)

    for row in rows:
        year = parse_year(row.get("publication_year", ""))
        labels = parse_technology_labels(
            row.get("technology_labels", "")
        )

        for label in labels:
            counts[label] += 1

            if year is not None:
                years[label].append(year)

    summary = []

    for label in sorted(counts):
        label_years = years[label]

        summary.append(
            {
                "technology_label": label,
                "publication_count": counts[label],
                "first_publication_year": (
                    min(label_years)
                    if label_years
                    else ""
                ),
                "latest_publication_year": (
                    max(label_years)
                    if label_years
                    else ""
                ),
            }
        )

    return summary


def print_summary(rows: list[dict[str, str]]) -> None:
    """Print high-level corpus and technology statistics."""
    valid_year_rows = 0
    missing_year_rows = 0
    labelled_rows = 0
    unlabelled_rows = 0
    multi_label_rows = 0
    technology_counts: Counter[str] = Counter()

    for row in rows:
        year = parse_year(row.get("publication_year", ""))

        if year is None:
            missing_year_rows += 1
        else:
            valid_year_rows += 1

        labels = parse_technology_labels(
            row.get("technology_labels", "")
        )

        if labels:
            labelled_rows += 1
            technology_counts.update(labels)
        else:
            unlabelled_rows += 1

        if len(labels) > 1:
            multi_label_rows += 1

    print(f"Input records: {len(rows)}")
    print(f"Records with valid year: {valid_year_rows}")
    print(f"Records without valid year: {missing_year_rows}")
    print(f"Records with technology label: {labelled_rows}")
    print(f"Records without technology label: {unlabelled_rows}")
    print(f"Records with multiple labels: {multi_label_rows}")

    print("\nTechnology totals")
    print("-" * 40)

    for label, count in sorted(
        technology_counts.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        print(f"{label}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyse publication growth by year, analysis tier "
            "and PFAS treatment technology."
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
        default=Path("data/processed/trends"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = read_csv(args.input)

    if not rows:
        raise ValueError("The analysis corpus contains no records")

    year_summary = build_year_summary(rows)
    year_tier_summary = build_year_tier_summary(rows)
    year_technology_summary = build_year_technology_summary(rows)
    technology_summary = build_technology_summary(rows)

    write_rows(
        year_summary,
        args.output_dir / "publications_by_year.csv",
        [
            "publication_year",
            "publication_count",
        ],
    )
    write_rows(
        year_tier_summary,
        args.output_dir / "publications_by_year_and_tier.csv",
        [
            "publication_year",
            "analysis_tier",
            "publication_count",
        ],
    )
    write_rows(
        year_technology_summary,
        args.output_dir
        / "publications_by_year_and_technology.csv",
        [
            "publication_year",
            "technology_label",
            "publication_count",
        ],
    )
    write_rows(
        technology_summary,
        args.output_dir / "technology_summary.csv",
        [
            "technology_label",
            "publication_count",
            "first_publication_year",
            "latest_publication_year",
        ],
    )

    print_summary(rows)
    print(f"\nSaved trend outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
