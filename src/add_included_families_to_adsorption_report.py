from __future__ import annotations

import csv
from pathlib import Path


FAMILY_SUMMARY_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_summary.csv"
)

REPORT_PATH = Path(
    "reports/patent-adsorption-pilot-summary.md"
)

SECTION_HEADING = "## Included patent families"

def read_family_rows() -> list[dict[str, str]]:
    """Read the adsorption patent-family summary."""
    with FAMILY_SUMMARY_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def is_included_family(
    row: dict[str, str],
) -> bool:
    """Return True when a family has an include decision."""
    decisions = {
        decision.strip()
        for decision in row.get(
            "decisions",
            "",
        ).split(";")
        if decision.strip()
    }

    return "include" in decisions

def clean_table_text(
    value: str,
) -> str:
    """Clean text so it renders safely in a Markdown table."""
    return (
        value.replace("|", "/")
        .replace("\n", " ")
        .strip()
    )


def build_included_family_section(
    rows: list[dict[str, str]],
) -> str:
    """Build a Markdown table of included patent families."""
    included_rows = [
        row
        for row in rows
        if is_included_family(row)
    ]

    included_rows.sort(
        key=lambda row: (
            row.get(
                "earliest_priority_date",
                "",
            ),
            row.get(
                "family_group",
                "",
            ),
        )
    )

    lines = [
        SECTION_HEADING,
        "",
        (
            f"The screening identified {len(included_rows)} "
            "included patent families."
        ),
        "",
        (
            "| Family | Representative title | Assignees | "
            "Priority date | Jurisdictions | Publications |"
        ),
        "|---|---|---|---|---|---:|",
    ]

    for row in included_rows:
        lines.append(
            "| "
            f"{clean_table_text(row.get('family_group', ''))} | "
            f"{clean_table_text(row.get('representative_title', ''))} | "
            f"{clean_table_text(row.get('assignees', ''))} | "
            f"{clean_table_text(row.get('earliest_priority_date', ''))} | "
            f"{clean_table_text(row.get('jurisdictions', ''))} | "
            f"{clean_table_text(row.get('publication_count', ''))} |"
        )

    return "\n".join(lines)

def replace_or_append_section(
    report_text: str,
    section_text: str,
) -> str:
    """Replace an existing section or append it to the report."""
    section_start = report_text.find(
        SECTION_HEADING
    )

    if section_start == -1:
        return (
            report_text.rstrip()
            + "\n\n"
            + section_text
            + "\n"
        )

    next_section_start = report_text.find(
        "\n## ",
        section_start + len(SECTION_HEADING),
    )

    if next_section_start == -1:
        return (
            report_text[:section_start].rstrip()
            + "\n\n"
            + section_text
            + "\n"
        )

    return (
        report_text[:section_start].rstrip()
        + "\n\n"
        + section_text
        + "\n"
        + report_text[next_section_start:]
    )

def main() -> None:
    """Add the included-family table to the adsorption report."""
    family_rows = read_family_rows()

    section_text = build_included_family_section(
        family_rows
    )

    report_text = REPORT_PATH.read_text(
        encoding="utf-8"
    )

    updated_report = replace_or_append_section(
        report_text,
        section_text,
    )

    REPORT_PATH.write_text(
        updated_report,
        encoding="utf-8",
    )

    included_count = sum(
        1
        for row in family_rows
        if is_included_family(row)
    )

    print(
        f"Included families added: {included_count}"
    )
    print(
        f"Report updated: {REPORT_PATH}"
    )


if __name__ == "__main__":
    main()

