from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


SCREENING_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening.csv"
)

FAMILY_SUMMARY_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_summary.csv"
)

REPORT_PATH = Path(
    "reports/patent-adsorption-pilot-summary.md"
)

def read_csv_rows(
    path: Path,
) -> list[dict[str, str]]:
    """Read all rows from a CSV file."""
    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def split_values(
    value: str,
) -> list[str]:
    """Split a semicolon-separated field into clean values."""
    return [
        item.strip()
        for item in value.split(";")
        if item.strip()
    ]

def count_screening_decisions(
    rows: list[dict[str, str]],
) -> Counter[str]:
    """Count screening decisions across publication records."""
    return Counter(
        row.get(
            "manual_relevance_decision",
            "",
        ).strip() or "blank"
        for row in rows
    )


def count_family_decisions(
    rows: list[dict[str, str]],
) -> Counter[str]:
    """Assign one consolidated decision to each patent family."""
    counts: Counter[str] = Counter()

    decision_priority = {
        "include": 0,
        "context_only": 1,
        "uncertain": 2,
        "exclude": 3,
        "blank": 4,
    }

    for row in rows:
        decisions = split_values(
            row.get(
                "decisions",
                "",
            )
        )

        if not decisions:
            counts["blank"] += 1
            continue

        family_decision = min(
            decisions,
            key=lambda decision: decision_priority.get(
                decision,
                5,
            ),
        )

        counts[family_decision] += 1

    return counts

def count_assignees(
    family_rows: list[dict[str, str]],
) -> Counter[str]:
    """Count assignee appearances across assigned patent families."""
    counts: Counter[str] = Counter()

    for row in family_rows:
        for assignee in split_values(
            row.get(
                "assignees",
                "",
            )
        ):
            counts[assignee] += 1

    return counts


def count_jurisdictions(
    family_rows: list[dict[str, str]],
) -> Counter[str]:
    """Count jurisdiction appearances across patent families."""
    counts: Counter[str] = Counter()

    for row in family_rows:
        for jurisdiction in split_values(
            row.get(
                "jurisdictions",
                "",
            )
        ):
            counts[jurisdiction] += 1

    return counts

def get_priority_date_range(
    family_rows: list[dict[str, str]],
) -> tuple[str, str]:
    """Return the earliest and latest family priority dates."""
    dates: list[str] = []

    for row in family_rows:
        earliest = row.get(
            "earliest_priority_date",
            "",
        ).strip()

        latest = row.get(
            "latest_priority_date",
            "",
        ).strip()

        if earliest:
            dates.append(earliest)

        if latest:
            dates.append(latest)

    if not dates:
        return "", ""

    dates.sort()

    return dates[0], dates[-1]


def get_multi_publication_families(
    family_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Return families represented by multiple publications."""
    return [
        row
        for row in family_rows
        if int(
            row.get(
                "publication_count",
                "0",
            )
            or 0
        ) > 1
    ]

def format_counter_lines(
    counts: Counter[str],
    limit: int | None = None,
) -> list[str]:
    """Format counter entries as Markdown bullet lines."""
    items = counts.most_common(
        limit
    )

    if not items:
        return [
            "- No data available."
        ]

    return [
        f"- {name}: {count}"
        for name, count in items
    ]


def build_report(
    screening_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
) -> str:
    """Build the adsorption patent-landscape Markdown report."""
    publication_decisions = count_screening_decisions(
        screening_rows
    )

    family_decisions = count_family_decisions(
        family_rows
    )

    assignee_counts = count_assignees(
        family_rows
    )

    jurisdiction_counts = count_jurisdictions(
        family_rows
    )

    earliest_date, latest_date = get_priority_date_range(
        family_rows
    )

    multi_publication_families = (
        get_multi_publication_families(
            family_rows
        )
    )

    lines = [
        "# Activated-Carbon PFAS Patent Pilot",
        "",
        "## Scope",
        "",
        (
            "This report summarizes the screened Google Patents "
            "pilot focused on activated-carbon and related "
            "adsorption approaches for PFAS treatment in water."
        ),
        "",
        "## Screening results",
        "",
        f"- Publication records reviewed: {len(screening_rows)}",
        f"- Assigned patent families: {len(family_rows)}",
        (
            "- Multi-publication families: "
            f"{len(multi_publication_families)}"
        ),
        "",
        "### Publication-level decisions",
        "",
        *format_counter_lines(
            publication_decisions
        ),
        "",
        "### Family-level decisions",
        "",
        *format_counter_lines(
            family_decisions
        ),
        "",
        "## Priority-date coverage",
        "",
        f"- Earliest priority date: {earliest_date or 'Unknown'}",
        f"- Latest priority date: {latest_date or 'Unknown'}",
        "",
        "## Leading assignees",
        "",
        *format_counter_lines(
            assignee_counts,
            limit=10,
        ),
        "",
        "## Jurisdiction coverage",
        "",
        *format_counter_lines(
            jurisdiction_counts,
            limit=15,
        ),
        "",
    ]

    return "\n".join(lines)

def write_report(
    report_text: str,
) -> Path:
    """Write the Markdown patent-landscape report."""
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        report_text,
        encoding="utf-8",
    )

    return REPORT_PATH


def main() -> None:
    """Generate the adsorption patent-landscape report."""
    screening_rows = read_csv_rows(
        SCREENING_PATH
    )

    family_rows = read_csv_rows(
        FAMILY_SUMMARY_PATH
    )

    report_text = build_report(
        screening_rows,
        family_rows,
    )

    output_path = write_report(
        report_text
    )

    print(
        f"Screening records: {len(screening_rows)}"
    )
    print(
        f"Patent families: {len(family_rows)}"
    )
    print(
        f"Report written to: {output_path}"
    )


if __name__ == "__main__":
    main()

