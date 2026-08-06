from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_uncertain_review.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_remaining_review.csv"
)

HIGH_PRIORITY_THRESHOLD = 2

def read_review_rows() -> list[dict[str, str]]:
    """Read the prioritized adsorption review dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def is_remaining_record(
    row: dict[str, str],
) -> bool:
    """Return True for lower-priority records still requiring review."""
    priority_text = row.get(
        "review_priority",
        "0",
    ).strip()

    priority = int(
        priority_text or 0
    )

    decision = row.get(
        "manual_relevance_decision",
        "",
    ).strip()

    return (
        priority < HIGH_PRIORITY_THRESHOLD
        and not decision
    )

def build_remaining_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Keep only lower-priority records still needing review."""
    remaining_rows = [
        dict(row)
        for row in rows
        if is_remaining_record(row)
    ]

    remaining_rows.sort(
        key=lambda row: (
            -int(
                row.get(
                    "review_priority",
                    "0",
                )
                or 0
            ),
            row.get(
                "publication_id",
                "",
            ),
        )
    )

    return remaining_rows

def write_remaining_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the lower-priority records still requiring review."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No remaining adsorption records were found."
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
    remaining_rows: list[dict[str, str]],
) -> None:
    """Print a short summary of the remaining-review dataset."""
    print(
        f"Source uncertain records: {len(source_rows)}"
    )

    print(
        f"Remaining lower-priority records: {len(remaining_rows)}"
    )

    priority_counts: dict[str, int] = {}

    for row in remaining_rows:
        priority = row.get(
            "review_priority",
            "0",
        ).strip() or "0"

        priority_counts[priority] = (
            priority_counts.get(priority, 0) + 1
        )

    for priority in sorted(
        priority_counts,
        key=int,
        reverse=True,
    ):
        print(
            f"Priority {priority}: "
            f"{priority_counts[priority]}"
        )


def main() -> None:
    """Build the remaining adsorption review file."""
    source_rows = read_review_rows()

    remaining_rows = build_remaining_rows(
        source_rows
    )

    output_path = write_remaining_csv(
        remaining_rows
    )

    print_summary(
        source_rows,
        remaining_rows,
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()

