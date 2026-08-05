from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_processed.csv"
)

OUTPUT_DIR = Path(
    "data/processed/patents/pat_eox_001"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "pat_eox_001_screening.csv"
)

def read_processed_rows() -> list[dict[str, str]]:
    """Read the normalized patent pilot dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def build_screening_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Create a manual patent-screening dataset."""
    screening_rows: list[dict[str, str]] = []

    for row in rows:
        screening_rows.append(
            {
                **row,
                "manual_relevance_decision": "",
                "manual_family_group": "",
                "manual_screening_notes": "",
            }
        )

    return screening_rows

def sort_screening_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Sort screening records by priority date and title."""
    return sorted(
        rows,
        key=lambda row: (
            row.get(
                "priority_date",
                "",
            )
            or "9999-99-99",
            row.get(
                "title",
                "",
            ),
            row.get(
                "publication_id",
                "",
            ),
        ),
    )


def write_screening_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the manual patent-screening file."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No patent records available for screening."
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

def main() -> None:
    """Build the manual patent-screening sample."""
    rows = read_processed_rows()

    screening_rows = build_screening_rows(
        rows
    )

    screening_rows = sort_screening_rows(
        screening_rows
    )

    output_path = write_screening_csv(
        screening_rows
    )

    print(
        f"Patent records prepared for screening: "
        f"{len(screening_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()

