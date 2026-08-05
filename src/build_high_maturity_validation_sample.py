from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/evidence_type/"
    "openalex_evidence_type_classified.csv"
)

OUTPUT_DIR = Path(
    "data/processed/high_maturity_validation"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "high_maturity_validation_sample.csv"
)

TARGET_EVIDENCE_TYPES = {
    "field_demonstration",
    "pilot",
}

def read_classified_rows() -> list[dict[str, str]]:
    """Read the evidence-classified publication corpus."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def is_high_maturity_record(
    row: dict[str, str],
) -> bool:
    """Return True for pilot or field-demonstration records."""
    evidence_type = row.get(
        "primary_evidence_type",
        "",
    ).strip()

    return evidence_type in TARGET_EVIDENCE_TYPES

def build_validation_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Create a focused sample for manual maturity validation."""
    validation_rows: list[dict[str, str]] = []

    for row in rows:
        if not is_high_maturity_record(row):
            continue

        validation_rows.append(
            {
                "openalex_id": row.get(
                    "openalex_id",
                    "",
                ),
                "title": row.get(
                    "title",
                    "",
                ),
                "publication_year": row.get(
                    "publication_year",
                    "",
                ),
                "technology_labels": row.get(
                    "technology_labels",
                    "",
                ),
                "primary_evidence_type": row.get(
                    "primary_evidence_type",
                    "",
                ),
                "doi": row.get(
                    "doi",
                    "",
                ),
                "openalex_url": (
                    f"https://openalex.org/"
                    f"{row.get('openalex_id', '').strip()}"
                    if row.get(
                        "openalex_id",
                        "",
                    ).strip()
                    else ""
                ),
                "abstract": row.get(
                    "abstract",
                    "",
                ),
                "manual_evidence_decision": "",
                "manual_scale": "",
                "manual_validation_notes": "",
            }
        )

    return validation_rows

def sort_validation_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Sort field records before pilot records, then by year."""
    evidence_priority = {
        "field_demonstration": 0,
        "pilot": 1,
    }

    return sorted(
        rows,
        key=lambda row: (
            evidence_priority.get(
                row["primary_evidence_type"],
                99,
            ),
            -int(
                row["publication_year"]
                or 0
            ),
            row["title"],
        ),
    )


def write_validation_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the manual validation sample."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "openalex_id",
        "title",
        "publication_year",
        "technology_labels",
        "primary_evidence_type",
        "doi",
        "openalex_url",
        "abstract",
        "manual_evidence_decision",
        "manual_scale",
        "manual_validation_notes",
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

def print_validation_summary(
    rows: list[dict[str, str]],
) -> None:
    """Print the number of records by evidence type."""
    counts = {
        evidence_type: 0
        for evidence_type in TARGET_EVIDENCE_TYPES
    }

    for row in rows:
        evidence_type = row[
            "primary_evidence_type"
        ]
        counts[evidence_type] += 1

    print(
        f"Validation records: {len(rows)}"
    )
    print(
        "Field demonstrations: "
        f"{counts['field_demonstration']}"
    )
    print(
        f"Pilot studies: {counts['pilot']}"
    )


def main() -> None:
    """Build the high-maturity validation sample."""
    rows = read_classified_rows()

    validation_rows = build_validation_rows(
        rows
    )

    validation_rows = sort_validation_rows(
        validation_rows
    )

    output_path = write_validation_csv(
        validation_rows
    )

    print_validation_summary(
        validation_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
