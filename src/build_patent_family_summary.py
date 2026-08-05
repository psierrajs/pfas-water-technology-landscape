from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_screening.csv"
)

OUTPUT_DIR = Path(
    "data/processed/patents/pat_eox_001"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "pat_eox_001_family_summary.csv"
)

INCLUDED_DECISIONS = {
    "include",
    "context_only",
}

def read_screening_rows() -> list[dict[str, str]]:
    """Read the completed patent-screening dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalized_family_group(
    row: dict[str, str],
) -> str:
    """Return the manual family group or a publication-level fallback."""
    family_group = row.get(
        "manual_family_group",
        "",
    ).strip()

    if family_group:
        return family_group

    return (
        "PUB-"
        + row.get(
            "publication_id",
            "",
        ).strip()
    )

def group_family_rows(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group included and context-only records by family."""
    grouped_rows: dict[
        str,
        list[dict[str, str]],
    ] = defaultdict(list)

    for row in rows:
        decision = row.get(
            "manual_relevance_decision",
            "",
        ).strip()

        if decision not in INCLUDED_DECISIONS:
            continue

        family_group = normalized_family_group(
            row
        )

        grouped_rows[
            family_group
        ].append(row)

    return grouped_rows

def choose_representative_row(
    family_rows: list[dict[str, str]],
) -> dict[str, str]:
    """Choose one representative publication for a patent family."""
    return sorted(
        family_rows,
        key=lambda row: (
            row.get(
                "priority_date",
                "",
            )
            or "9999-99-99",
            row.get(
                "publication_date",
                "",
            )
            or "9999-99-99",
            row.get(
                "publication_id",
                "",
            ),
        ),
    )[0]


def unique_join(
    values: list[str],
) -> str:
    """Join unique non-empty values while preserving order."""
    seen: set[str] = set()
    output: list[str] = []

    for value in values:
        value = value.strip()

        if not value or value in seen:
            continue

        seen.add(value)
        output.append(value)

    return " | ".join(output)

def build_family_summary_rows(
    grouped_rows: dict[
        str,
        list[dict[str, str]],
    ],
) -> list[dict[str, Any]]:
    """Create one summary row for each patent family."""
    family_summary_rows: list[
        dict[str, Any]
    ] = []

    for family_group, family_rows in grouped_rows.items():
        representative = choose_representative_row(
            family_rows
        )

        publication_ids = unique_join(
            [
                row.get(
                    "publication_id",
                    "",
                )
                for row in family_rows
            ]
        )

        assignees = unique_join(
            [
                row.get(
                    "assignee_original",
                    "",
                )
                for row in family_rows
            ]
        )

        source_urls = unique_join(
            [
                row.get(
                    "source_url",
                    "",
                )
                for row in family_rows
            ]
        )

        decisions = unique_join(
            [
                row.get(
                    "manual_relevance_decision",
                    "",
                )
                for row in family_rows
            ]
        )

        family_summary_rows.append(
            {
                "family_group": family_group,
                "representative_publication_id": (
                    representative.get(
                        "publication_id",
                        "",
                    )
                ),
                "title": representative.get(
                    "title",
                    "",
                ),
                "assignees": assignees,
                "earliest_priority_date": min(
                    [
                        row.get(
                            "priority_date",
                            "",
                        )
                        for row in family_rows
                        if row.get(
                            "priority_date",
                            "",
                        )
                    ],
                    default="",
                ),
                "publication_count": len(
                    family_rows
                ),
                "publication_ids": publication_ids,
                "source_urls": source_urls,
                "manual_relevance_decisions": (
                    decisions
                ),
                "technology_labels": (
                    representative.get(
                        "technology_labels",
                        "",
                    )
                ),
            }
        )

    return family_summary_rows

def sort_family_summary_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort patent families by priority date and title."""
    return sorted(
        rows,
        key=lambda row: (
            row["earliest_priority_date"]
            or "9999-99-99",
            row["title"],
            row["family_group"],
        ),
    )


def write_family_summary_csv(
    rows: list[dict[str, Any]],
) -> Path:
    """Write the patent-family summary dataset."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "family_group",
        "representative_publication_id",
        "title",
        "assignees",
        "earliest_priority_date",
        "publication_count",
        "publication_ids",
        "source_urls",
        "manual_relevance_decisions",
        "technology_labels",
    ]

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    return OUTPUT_PATH

def print_family_summary(
    screening_rows: list[dict[str, str]],
    family_rows: list[dict[str, Any]],
) -> None:
    """Print a short patent-family consolidation summary."""
    included_records = [
        row
        for row in screening_rows
        if row.get(
            "manual_relevance_decision",
            "",
        ).strip()
        in INCLUDED_DECISIONS
    ]

    multi_publication_families = [
        row
        for row in family_rows
        if row["publication_count"] > 1
    ]

    print(
        f"Screened patent records read: "
        f"{len(screening_rows)}"
    )
    print(
        f"Included or context-only records: "
        f"{len(included_records)}"
    )
    print(
        f"Patent families created: "
        f"{len(family_rows)}"
    )
    print(
        f"Families with multiple publications: "
        f"{len(multi_publication_families)}"
    )


def main() -> None:
    """Build the patent-family summary."""
    screening_rows = read_screening_rows()

    grouped_rows = group_family_rows(
        screening_rows
    )

    family_rows = build_family_summary_rows(
        grouped_rows
    )

    family_rows = sort_family_summary_rows(
        family_rows
    )

    output_path = write_family_summary_csv(
        family_rows
    )

    print_family_summary(
        screening_rows,
        family_rows,
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
