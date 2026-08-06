from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_auto_screened.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_uncertain_review.csv"
)

TARGET_DECISION = "uncertain"

def read_uncertain_rows() -> list[dict[str, str]]:
    """Read only records marked uncertain."""
    uncertain_rows: list[dict[str, str]] = []

    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            decision = row.get(
                "manual_relevance_decision",
                "",
            ).strip()

            if decision == TARGET_DECISION:
                uncertain_rows.append(row)

    return uncertain_rows

def calculate_review_priority(
    row: dict[str, str],
) -> int:
    """Assign a simple priority score for manual review."""
    title = row.get(
        "title",
        "",
    ).lower()

    score = 0

    high_value_terms = (
        "pfas",
        "pfoa",
        "pfos",
        "perfluoroalkyl",
        "polyfluoroalkyl",
        "activated carbon",
        "granular activated carbon",
        "powdered activated carbon",
        "groundwater",
        "wastewater",
        "drinking water",
        "leachate",
        "remediation",
        "adsorption",
        "removal",
    )

    for term in high_value_terms:
        if term in title:
            score += 1

    return score


def sort_uncertain_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Sort likely relevant uncertain records first."""
    return sorted(
        rows,
        key=lambda row: (
            calculate_review_priority(row),
            row.get(
                "priority_date",
                "",
            ),
            row.get(
                "title",
                "",
            ),
        ),
        reverse=True,
    )

def calculate_review_priority(
    row: dict[str, str],
) -> int:
    """Assign a simple priority score for manual review."""
    title = row.get(
        "title",
        "",
    ).lower()

    score = 0

    high_value_terms = (
        "pfas",
        "pfoa",
        "pfos",
        "perfluoroalkyl",
        "polyfluoroalkyl",
        "activated carbon",
        "granular activated carbon",
        "powdered activated carbon",
        "groundwater",
        "wastewater",
        "drinking water",
        "leachate",
        "remediation",
        "adsorption",
        "removal",
    )

    for term in high_value_terms:
        if term in title:
            score += 1

    return score


def sort_uncertain_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Sort likely relevant uncertain records first."""
    return sorted(
        rows,
        key=lambda row: (
            calculate_review_priority(row),
            row.get(
                "priority_date",
                "",
            ),
            row.get(
                "title",
                "",
            ),
        ),
        reverse=True,
    )

def build_review_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Create a compact manual-review dataset."""
    review_rows: list[dict[str, str]] = []

    for row in rows:
        review_rows.append(
            {
                "review_priority": str(
                    calculate_review_priority(row)
                ),
                "publication_id": row.get(
                    "publication_id",
                    "",
                ),
                "title": row.get(
                    "title",
                    "",
                ),
                "assignee_original": row.get(
                    "assignee_original",
                    "",
                ),
                "priority_date": row.get(
                    "priority_date",
                    "",
                ),
                "source_url": row.get(
                    "source_url",
                    "",
                ),
                "manual_relevance_decision": "",
                "manual_family_group": "",
                "manual_screening_notes": "",
            }
        )

    return review_rows

def write_review_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the compact uncertain-record review file."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "review_priority",
        "publication_id",
        "title",
        "assignee_original",
        "priority_date",
        "source_url",
        "manual_relevance_decision",
        "manual_family_group",
        "manual_screening_notes",
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

def main() -> None:
    """Build the prioritized uncertain-record review file."""
    uncertain_rows = read_uncertain_rows()

    uncertain_rows = sort_uncertain_rows(
        uncertain_rows
    )

    review_rows = build_review_rows(
        uncertain_rows
    )

    output_path = write_review_csv(
        review_rows
    )

    print(
        f"Uncertain records prepared for review: "
        f"{len(review_rows)}"
    )

    if review_rows:
        priorities = [
            int(row["review_priority"])
            for row in review_rows
        ]

        print(
            "Review-priority range: "
            f"{min(priorities)} to {max(priorities)}"
        )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
    