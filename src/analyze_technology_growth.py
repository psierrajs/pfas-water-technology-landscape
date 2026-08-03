from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any


START_YEAR = 2018
COMPLETE_END_YEAR = 2025

EARLY_PERIOD = range(2018, 2021)
RECENT_PERIOD = range(2023, 2026)


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read annual technology publication counts."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def parse_rows(
    rows: list[dict[str, str]],
) -> dict[str, Counter[int]]:
    """Organize publication counts by technology and year."""
    technology_years: dict[str, Counter[int]] = {}

    for row in rows:
        technology = row.get(
            "technology_label",
            "",
        ).strip()

        if not technology:
            continue

        try:
            year = int(row["publication_year"])
            count = int(row["publication_count"])
        except (KeyError, ValueError):
            continue

        if technology not in technology_years:
            technology_years[technology] = Counter()

        technology_years[technology][year] += count

    return technology_years


def calculate_cagr(
    start_count: int,
    end_count: int,
    number_of_years: int,
) -> float | None:
    """Calculate CAGR when both endpoint counts are positive."""
    if (
        start_count <= 0
        or end_count <= 0
        or number_of_years <= 0
    ):
        return None

    return (
        (end_count / start_count)
        ** (1 / number_of_years)
        - 1
    )


def build_summary(
    technology_years: dict[str, Counter[int]],
) -> list[dict[str, Any]]:
    """Calculate growth indicators for every technology."""
    summary = []

    for technology, counts in technology_years.items():
        complete_counts = {
            year: counts.get(year, 0)
            for year in range(
                START_YEAR,
                COMPLETE_END_YEAR + 1,
            )
        }

        total_complete_period = sum(
            complete_counts.values()
        )
        early_total = sum(
            counts.get(year, 0)
            for year in EARLY_PERIOD
        )
        recent_total = sum(
            counts.get(year, 0)
            for year in RECENT_PERIOD
        )

        early_average = early_total / len(EARLY_PERIOD)
        recent_average = recent_total / len(RECENT_PERIOD)

        if early_average > 0:
            recent_to_early_ratio = (
                recent_average / early_average
            )
        else:
            recent_to_early_ratio = None

        peak_year, peak_count = max(
            complete_counts.items(),
            key=lambda item: (item[1], item[0]),
        )

        start_count = counts.get(START_YEAR, 0)
        end_count = counts.get(COMPLETE_END_YEAR, 0)

        cagr = calculate_cagr(
            start_count,
            end_count,
            COMPLETE_END_YEAR - START_YEAR,
        )

        summary.append(
            {
                "technology_label": technology,
                "total_2018_2025": total_complete_period,
                "early_total_2018_2020": early_total,
                "recent_total_2023_2025": recent_total,
                "early_annual_average": (
                    f"{early_average:.2f}"
                ),
                "recent_annual_average": (
                    f"{recent_average:.2f}"
                ),
                "recent_to_early_ratio": (
                    f"{recent_to_early_ratio:.2f}"
                    if recent_to_early_ratio is not None
                    else ""
                ),
                "count_2018": start_count,
                "count_2025": end_count,
                "cagr_2018_2025": (
                    f"{cagr:.4f}"
                    if cagr is not None
                    else ""
                ),
                "peak_year": peak_year,
                "peak_count": peak_count,
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["recent_total_2023_2025"]),
            str(row["technology_label"]),
        )
    )

    return summary


def write_csv(
    rows: list[dict[str, Any]],
    path: Path,
) -> None:
    """Write the technology-growth summary."""
    if not rows:
        raise ValueError("No technology summaries to write")

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
    """Print the principal growth indicators."""
    print(
        "Technology".ljust(32)
        + "Recent".rjust(9)
        + "Early".rjust(9)
        + "Ratio".rjust(10)
        + "Peak".rjust(12)
    )

    print("-" * 72)

    for row in rows:
        ratio = row["recent_to_early_ratio"] or "n/a"
        peak = (
            f"{row['peak_year']}:"
            f"{row['peak_count']}"
        )

        print(
            str(row["technology_label"])[:31].ljust(32)
            + str(
                row["recent_total_2023_2025"]
            ).rjust(9)
            + str(
                row["early_total_2018_2020"]
            ).rjust(9)
            + str(ratio).rjust(10)
            + peak.rjust(12)
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate annual growth indicators for PFAS "
            "treatment technology categories."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/processed/trends/"
            "publications_by_year_and_technology.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/processed/trends/"
            "technology_growth_summary.csv"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    technology_years = parse_rows(rows)
    summary = build_summary(technology_years)

    write_csv(summary, args.output)
    print_summary(summary)

    print(f"\nTechnologies analysed: {len(summary)}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
