from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


SCREENING_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_screening.csv"
)

FAMILY_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_family_summary.csv"
)

OUTPUT_PATH = Path(
    "reports/patent-eox-pilot-summary.md"
)

def read_csv_rows(
    path: Path,
) -> list[dict[str, str]]:
    """Read a UTF-8 CSV file into a list of rows."""
    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def count_screening_decisions(
    rows: list[dict[str, str]],
) -> Counter[str]:
    """Count manual patent-screening decisions."""
    return Counter(
        row.get(
            "manual_relevance_decision",
            "",
        ).strip()
        or "blank"
        for row in rows
    )

def count_families_by_assignee(
    family_rows: list[dict[str, str]],
) -> Counter[str]:
    """Count retained patent families by assignee."""
    counts: Counter[str] = Counter()

    for row in family_rows:
        assignees = row.get(
            "assignees",
            "",
        )

        for assignee in assignees.split("|"):
            assignee = assignee.strip()

            if assignee:
                counts[assignee] += 1

    return counts


def count_families_by_priority_year(
    family_rows: list[dict[str, str]],
) -> Counter[str]:
    """Count patent families by earliest priority year."""
    counts: Counter[str] = Counter()

    for row in family_rows:
        priority_date = row.get(
            "earliest_priority_date",
            "",
        ).strip()

        if not priority_date:
            counts["unknown"] += 1
            continue

        counts[priority_date[:4]] += 1

    return counts

def format_counter_bullets(
    counts: Counter[str],
) -> list[str]:
    """Convert counter values into Markdown bullets."""
    return [
        f"- `{label}`: {count}"
        for label, count in counts.most_common()
    ]


def format_family_table(
    family_rows: list[dict[str, str]],
) -> list[str]:
    """Create a Markdown table of retained patent families."""
    lines = [
        (
            "| Family | Priority | Assignee | "
            "Representative publication | Title |"
        ),
        "|---|---|---|---|---|",
    ]

    for row in family_rows:
        title = row.get(
            "title",
            "",
        ).replace(
            "|",
            "\\|",
        )

        assignees = row.get(
            "assignees",
            "",
        ).replace(
            "|",
            ", ",
        )

        lines.append(
            "| "
            f"{row.get('family_group', '')} | "
            f"{row.get('earliest_priority_date', '')} | "
            f"{assignees} | "
            f"{row.get('representative_publication_id', '')} | "
            f"{title} |"
        )

    return lines

def build_report(
    screening_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
) -> str:
    """Build the electrochemical-oxidation patent pilot report."""
    decision_counts = count_screening_decisions(
        screening_rows
    )

    assignee_counts = count_families_by_assignee(
        family_rows
    )

    priority_year_counts = (
        count_families_by_priority_year(
            family_rows
        )
    )

    multi_publication_families = [
        row
        for row in family_rows
        if int(
            row.get(
                "publication_count",
                "0",
            )
            or 0
        )
        > 1
    ]

    lines = [
        "# Electrochemical Oxidation Patent Pilot Summary",
        "",
        "## Purpose",
        "",
        (
            "This report summarizes the pilot patent search "
            "for electrochemical PFAS treatment technologies."
        ),
        "",
        "## Screening results",
        "",
        f"- Patent publications screened: {len(screening_rows)}",
        f"- Retained patent families: {len(family_rows)}",
        (
            "- Families with multiple jurisdictional "
            f"publications: {len(multi_publication_families)}"
        ),
        "",
        "### Manual relevance decisions",
        "",
        *format_counter_bullets(
            decision_counts
        ),
        "",
        "## Patent families by earliest priority year",
        "",
        *format_counter_bullets(
            Counter(
                dict(
                    sorted(
                        priority_year_counts.items()
                    )
                )
            )
        ),
        "",
        "## Leading assignees in the pilot set",
        "",
        *format_counter_bullets(
            assignee_counts
        ),
        "",
        "## Retained patent families",
        "",
        *format_family_table(
            family_rows
        ),
        "",
    ]

    return "\n".join(lines)

def write_report(
    report: str,
) -> Path:
    """Write the Markdown patent pilot report."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        report,
        encoding="utf-8",
    )

    return OUTPUT_PATH


def main() -> None:
    """Summarize the electrochemical patent pilot."""
    screening_rows = read_csv_rows(
        SCREENING_PATH
    )

    family_rows = read_csv_rows(
        FAMILY_PATH
    )

    report = build_report(
        screening_rows,
        family_rows,
    )

    output_path = write_report(
        report
    )

    print(
        f"Screened publications summarized: "
        f"{len(screening_rows)}"
    )
    print(
        f"Patent families summarized: "
        f"{len(family_rows)}"
    )
    print(
        f"Report written to: {output_path}"
    )


if __name__ == "__main__":
    main()

