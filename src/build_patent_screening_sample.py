from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_INPUT_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_processed.csv"
)

DEFAULT_OUTPUT_PATH = Path(
    "data/processed/patents/pat_eox_001/"
    "pat_eox_001_screening.csv"
)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line options for a screening dataset."""
    parser = argparse.ArgumentParser(
        description=(
            "Build a manual screening file from "
            "a processed patent dataset."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to the processed patent CSV.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path for the screening CSV.",
    )

    return parser.parse_args()

def read_processed_rows(
    input_path: Path,
) -> list[dict[str, str]]:
    """Read a normalized patent dataset."""
    with input_path.open(
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
    output_path: Path,
) -> Path:
    """Write the manual patent-screening file."""
    output_path.parent.mkdir(
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

    with output_path.open(
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

    return output_path
    
def main() -> None:
    """Build a manual patent-screening sample."""
    args = parse_arguments()

    rows = read_processed_rows(
        args.input
    )

    screening_rows = build_screening_rows(
        rows
    )

    screening_rows = sort_screening_rows(
        screening_rows
    )

    output_path = write_screening_csv(
        screening_rows,
        args.output,
    )

    print(
        "Patent records prepared for screening: "
        f"{len(screening_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )

if __name__ == "__main__":
    main()

