from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_summary.csv"
)

def read_screening_rows() -> list[dict[str, str]]:
    """Read the consolidated adsorption screening dataset."""
    with INPUT_PATH.open(
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

def first_nonempty(
    rows: list[dict[str, str]],
    field: str,
) -> str:
    """Return the first non-empty value for a field."""
    for row in rows:
        value = row.get(
            field,
            "",
        ).strip()

        if value:
            return value

    return ""


def collect_unique_values(
    rows: list[dict[str, str]],
    field: str,
) -> list[str]:
    """Collect unique semicolon-separated values from a field."""
    values: set[str] = set()

    for row in rows:
        for value in split_values(
            row.get(
                field,
                "",
            )
        ):
            values.add(value)

    return sorted(values)

def group_rows_by_family(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group records by assigned adsorption family."""
    families: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        family_group = row.get(
            "manual_family_group",
            "",
        ).strip()

        if not family_group:
            continue

        families.setdefault(
            family_group,
            [],
        ).append(row)

    return families


def extract_jurisdiction(
    publication_id: str,
) -> str:
    """Extract the publication jurisdiction prefix."""
    publication_id = publication_id.strip()

    if not publication_id:
        return ""

    return publication_id.split(
        "-",
        maxsplit=1,
    )[0]

def build_family_summary_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build one summary row per assigned patent family."""
    families = group_rows_by_family(
        rows
    )

    summary_rows: list[dict[str, str]] = []

    for family_group, family_rows in families.items():
        publication_ids = sorted(
            {
                row.get(
                    "publication_id",
                    "",
                ).strip()
                for row in family_rows
                if row.get(
                    "publication_id",
                    "",
                ).strip()
            }
        )

        jurisdictions = sorted(
            {
                extract_jurisdiction(
                    publication_id
                )
                for publication_id in publication_ids
                if extract_jurisdiction(
                    publication_id
                )
            }
        )

        decisions = sorted(
            {
                row.get(
                    "manual_relevance_decision",
                    "",
                ).strip()
                for row in family_rows
                if row.get(
                    "manual_relevance_decision",
                    "",
                ).strip()
            }
        )

        assignees = collect_unique_values(
            family_rows,
            "assignee_original",
        )

        priority_dates = sorted(
            {
                row.get(
                    "priority_date",
                    "",
                ).strip()
                for row in family_rows
                if row.get(
                    "priority_date",
                    "",
                ).strip()
            }
        )

        summary_rows.append(
            {
                "family_group": family_group,
                "publication_count": str(
                    len(publication_ids)
                ),
                "publication_ids": "; ".join(
                    publication_ids
                ),
                "jurisdictions": "; ".join(
                    jurisdictions
                ),
                "decisions": "; ".join(
                    decisions
                ),
                "representative_title": first_nonempty(
                    family_rows,
                    "title",
                ),
                "assignees": "; ".join(
                    assignees
                ),
                "earliest_priority_date": (
                    priority_dates[0]
                    if priority_dates
                    else ""
                ),
                "latest_priority_date": (
                    priority_dates[-1]
                    if priority_dates
                    else ""
                ),
            }
        )

    return sorted(
        summary_rows,
        key=lambda row: row["family_group"],
    )

def write_family_summary(
    rows: list[dict[str, str]],
) -> Path:
    """Write the adsorption patent-family summary."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No assigned adsorption patent families were found."
        )

    fieldnames = list(
        rows[0].keys()
    )

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


def print_summary(
    source_rows: list[dict[str, str]],
    family_rows: list[dict[str, str]],
) -> None:
    """Print a short family-summary report."""
    multi_publication_families = sum(
        1
        for row in family_rows
        if int(row["publication_count"]) > 1
    )

    print(
        f"Source screening records: {len(source_rows)}"
    )
    print(
        f"Assigned patent families: {len(family_rows)}"
    )
    print(
        "Multi-publication families: "
        f"{multi_publication_families}"
    )


def main() -> None:
    """Build the adsorption patent-family summary."""
    source_rows = read_screening_rows()

    family_rows = build_family_summary_rows(
        source_rows
    )

    output_path = write_family_summary(
        family_rows
    )

    print_summary(
        source_rows,
        family_rows,
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()

