from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any


DEFAULT_INPUT_PATH = Path(
    "data/raw/patents/"
    "pat_eox_001_google_patents.csv"
)

DEFAULT_OUTPUT_PATH = Path(
    "data/processed/patents/"
    "pat_eox_001/"
    "pat_eox_001_processed.csv"
)

DEFAULT_QUERY_ID = "PAT-EOX-001"

DEFAULT_TECHNOLOGY_LABEL = (
    "electrochemical_oxidation"
)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line options for a patent export."""
    parser = argparse.ArgumentParser(
        description=(
            "Process a Google Patents CSV export."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to the raw Google Patents CSV export.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path for the processed CSV output.",
    )

    parser.add_argument(
        "--query-id",
        default=DEFAULT_QUERY_ID,
        help="Stable identifier for the patent search.",
    )

    parser.add_argument(
        "--technology-label",
        default=DEFAULT_TECHNOLOGY_LABEL,
        help="Technology label assigned to each record.",
    )

    return parser.parse_args()
    
def read_google_patents_rows(
    input_path: Path,
) -> list[dict[str, str]]:
    """Read a Google Patents CSV export with a metadata first line."""
    with input_path.open(
        encoding="utf-8-sig",
        newline="",
    ) as file:
        next(file)

        reader = csv.DictReader(file)
        return list(reader)


def normalize_text(
    value: str,
) -> str:
    """Trim surrounding whitespace and collapse internal spaces."""
    return " ".join(value.split())

def build_processed_rows(
    rows: list[dict[str, str]],
    query_id: str,
    technology_label: str,
) -> list[dict[str, Any]]:
    """Convert raw Google Patents rows into a normalized pilot dataset."""
    processed_rows: list[dict[str, Any]] = []

    for row in rows:
        publication_id = normalize_text(
            row.get(
                "id",
                "",
            )
        )

        if not publication_id:
            continue

        processed_rows.append(
            {
                "query_id": query_id,
                "publication_id": publication_id,
                "title": normalize_text(
                    row.get(
                        "title",
                        "",
                    )
                ),
                "assignee_original": normalize_text(
                    row.get(
                        "assignee",
                        "",
                    )
                ),
                "inventors": normalize_text(
                    row.get(
                        "inventor/author",
                        "",
                    )
                ),
                "priority_date": normalize_text(
                    row.get(
                        "priority date",
                        "",
                    )
                ),
                "filing_date": normalize_text(
                    row.get(
                        "filing/creation date",
                        "",
                    )
                ),
                "publication_date": normalize_text(
                    row.get(
                        "publication date",
                        "",
                    )
                ),
                "grant_date": normalize_text(
                    row.get(
                        "grant date",
                        "",
                    )
                ),
                "source_url": normalize_text(
                    row.get(
                        "result link",
                        "",
                    )
                ),
                "technology_labels": technology_label,
                "relevance_label": "",
                "family_group": "",
                "manual_review_notes": "",
            }
        )

    return processed_rows

def sort_processed_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort patent records by priority date and title."""
    return sorted(
        rows,
        key=lambda row: (
            row["priority_date"] or "9999-99-99",
            row["title"],
            row["publication_id"],
        ),
    )


def write_processed_csv(
    rows: list[dict[str, Any]],
    output_path: Path,
) -> Path:
    """Write the normalized patent pilot dataset."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "query_id",
        "publication_id",
        "title",
        "assignee_original",
        "inventors",
        "priority_date",
        "filing_date",
        "publication_date",
        "grant_date",
        "source_url",
        "technology_labels",
        "relevance_label",
        "family_group",
        "manual_review_notes",
    ]

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
def print_processing_summary(
    raw_rows: list[dict[str, str]],
    processed_rows: list[dict[str, Any]],
) -> None:
    """Print a short summary of the patent export processing."""
    assignees = {
        row["assignee_original"]
        for row in processed_rows
        if row["assignee_original"]
    }

    priority_dates = [
        row["priority_date"]
        for row in processed_rows
        if row["priority_date"]
    ]

    print(
        f"Raw rows read: {len(raw_rows)}"
    )
    print(
        f"Processed patent records: {len(processed_rows)}"
    )
    print(
        f"Distinct assignee names: {len(assignees)}"
    )

    if priority_dates:
        print(
            "Priority-date range: "
            f"{min(priority_dates)} to "
            f"{max(priority_dates)}"
        )


def main() -> None:
    """Process a Google Patents export."""
    args = parse_arguments()

    raw_rows = read_google_patents_rows(
        args.input
    )

    processed_rows = build_processed_rows(
        raw_rows,
        args.query_id,
        args.technology_label,
    )

    processed_rows = sort_processed_rows(
        processed_rows
    )

    output_path = write_processed_csv(
        processed_rows,
        args.output,
    )

    print_processing_summary(
        raw_rows,
        processed_rows,
    )

    print(
        f"Query ID: {args.query_id}"
    )
    print(
        "Technology label: "
        f"{args.technology_label}"
    )
    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()

