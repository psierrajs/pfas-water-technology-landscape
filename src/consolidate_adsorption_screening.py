from __future__ import annotations

import csv
from pathlib import Path


HIGH_PRIORITY_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_high_priority_prefilled.csv"
)

REMAINING_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_remaining_review_prefilled.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening.csv"
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


def combine_rows(
    high_priority_rows: list[dict[str, str]],
    remaining_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Combine both reviewed adsorption subsets."""
    combined_rows = [
        *high_priority_rows,
        *remaining_rows,
    ]

    publication_ids = [
        row.get(
            "publication_id",
            "",
        ).strip()
        for row in combined_rows
    ]

    duplicate_ids = {
        publication_id
        for publication_id in publication_ids
        if publication_id
        and publication_ids.count(publication_id) > 1
    }

    if duplicate_ids:
        duplicate_text = ", ".join(
            sorted(duplicate_ids)
        )

        raise ValueError(
            "Duplicate publication IDs found: "
            f"{duplicate_text}"
        )

    return combined_rows

def sort_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Sort records by decision and publication ID."""
    decision_order = {
        "include": 0,
        "context_only": 1,
        "uncertain": 2,
        "exclude": 3,
        "": 4,
    }

    return sorted(
        rows,
        key=lambda row: (
            decision_order.get(
                row.get(
                    "manual_relevance_decision",
                    "",
                ).strip(),
                5,
            ),
            row.get(
                "manual_family_group",
                "",
            ).strip(),
            row.get(
                "publication_id",
                "",
            ).strip(),
        ),
    )

def write_consolidated_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the consolidated adsorption screening dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No adsorption screening records were found."
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
    rows: list[dict[str, str]],
) -> None:
    """Print decision and family counts."""
    decision_counts: dict[str, int] = {}
    family_groups: set[str] = set()

    for row in rows:
        decision = row.get(
            "manual_relevance_decision",
            "",
        ).strip() or "blank"

        decision_counts[decision] = (
            decision_counts.get(decision, 0) + 1
        )

        family_group = row.get(
            "manual_family_group",
            "",
        ).strip()

        if family_group:
            family_groups.add(family_group)

    print(
        f"Consolidated records: {len(rows)}"
    )

    for decision in (
        "include",
        "context_only",
        "uncertain",
        "exclude",
        "blank",
    ):
        if decision in decision_counts:
            print(
                f"{decision}: "
                f"{decision_counts[decision]}"
            )

    print(
        f"Assigned family groups: {len(family_groups)}"
    )


def main() -> None:
    """Build the consolidated adsorption screening dataset."""
    high_priority_rows = read_csv_rows(
        HIGH_PRIORITY_PATH
    )

    remaining_rows = read_csv_rows(
        REMAINING_PATH
    )

    combined_rows = combine_rows(
        high_priority_rows,
        remaining_rows,
    )

    sorted_rows = sort_rows(
        combined_rows
    )

    output_path = write_consolidated_csv(
        sorted_rows
    )

    print_summary(
        sorted_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
