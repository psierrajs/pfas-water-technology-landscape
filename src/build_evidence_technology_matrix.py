from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/evidence_type/"
    "openalex_evidence_type_classified.csv"
)

OUTPUT_DIR = Path(
    "data/processed/evidence_technology_matrix"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "evidence_type_by_technology.csv"
)

PRIMARY_EVIDENCE_TYPES = (
    "field_demonstration",
    "pilot",
    "life_cycle_assessment",
    "computational",
    "mechanistic",
    "experimental",
    "review",
    "other",
)

def split_technology_labels(
    value: str,
) -> list[str]:
    """Split the serialized technology-label field."""
    if not value.strip():
        return []

    for separator in (
        "|",
        ";",
    ):
        if separator in value:
            return [
                label.strip()
                for label in value.split(separator)
                if label.strip()
            ]

    return [value.strip()]


def read_classified_rows() -> list[dict[str, str]]:
    """Read the evidence-classified publication corpus."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))

def build_evidence_technology_rows(
    rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[str],
]:
    """Aggregate publication counts by technology and evidence type."""
    publication_sets: dict[
        str,
        dict[str, set[str]],
    ] = defaultdict(
        lambda: defaultdict(set)
    )

    technologies: set[str] = set()

    for row in rows:
        openalex_id = row.get(
            "openalex_id",
            "",
        ).strip()

        if not openalex_id:
            continue

        primary_evidence_type = row.get(
            "primary_evidence_type",
            "other",
        ).strip()

        if (
            primary_evidence_type
            not in PRIMARY_EVIDENCE_TYPES
        ):
            primary_evidence_type = "other"

        labels = split_technology_labels(
            row.get(
                "technology_labels",
                "",
            )
        )

        for technology in labels:
            technologies.add(technology)

            publication_sets[
                technology
            ][primary_evidence_type].add(
                openalex_id
            )

    evidence_columns = list(
        PRIMARY_EVIDENCE_TYPES
    )

    output_rows: list[dict[str, Any]] = []

    for technology in sorted(technologies):
        evidence_sets = publication_sets[
            technology
        ]

        row: dict[str, Any] = {
            "technology": technology,
        }

        total_publications: set[str] = set()

        for evidence_type in evidence_columns:
            publications = evidence_sets.get(
                evidence_type,
                set(),
            )

            row[evidence_type] = len(
                publications
            )

            total_publications.update(
                publications
            )

        row["total_unique_publications"] = len(
            total_publications
        )

        output_rows.append(row)

    return (
        output_rows,
        evidence_columns,
    )

def sort_evidence_technology_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort technologies by maturity evidence and volume."""
    return sorted(
        rows,
        key=lambda row: (
            row["field_demonstration"],
            row["pilot"],
            row["life_cycle_assessment"],
            row["experimental"],
            row["total_unique_publications"],
            row["technology"],
        ),
        reverse=True,
    )


def write_evidence_technology_csv(
    rows: list[dict[str, Any]],
    evidence_columns: list[str],
) -> Path:
    """Write the evidence-type-by-technology matrix."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "technology",
        "total_unique_publications",
        *evidence_columns,
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

def print_evidence_technology_summary(
    rows: list[dict[str, Any]],
) -> None:
    """Print evidence maturity by technology."""
    print(
        "\nEvidence maturity by technology"
    )
    print("-" * 120)

    for row in rows:
        print(
            f"{row['field_demonstration']:>2} field | "
            f"{row['pilot']:>2} pilot | "
            f"{row['life_cycle_assessment']:>2} LCA | "
            f"{row['experimental']:>3} experimental | "
            f"{row['computational']:>2} computational | "
            f"{row['mechanistic']:>2} mechanistic | "
            f"{row['review']:>3} review | "
            f"{row['total_unique_publications']:>3} total | "
            f"{row['technology']}"
        )


def print_high_maturity_technologies(
    rows: list[dict[str, Any]],
) -> None:
    """Print technologies with pilot or field evidence."""
    high_maturity_rows = [
        row
        for row in rows
        if (
            row["field_demonstration"] > 0
            or row["pilot"] > 0
        )
    ]

    print(
        "\nTechnologies with pilot or field evidence"
    )
    print("-" * 100)

    for row in high_maturity_rows:
        print(
            f"{row['field_demonstration']:>2} field | "
            f"{row['pilot']:>2} pilot | "
            f"{row['total_unique_publications']:>3} total | "
            f"{row['technology']}"
        )

def main() -> None:
    """Build the evidence-type-by-technology matrix."""
    rows = read_classified_rows()

    matrix_rows, evidence_columns = (
        build_evidence_technology_rows(rows)
    )

    matrix_rows = sort_evidence_technology_rows(
        matrix_rows
    )

    output_path = write_evidence_technology_csv(
        matrix_rows,
        evidence_columns,
    )

    print(
        f"Classified publications read: {len(rows)}"
    )
    print(
        f"Technologies in matrix: {len(matrix_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )

    print_evidence_technology_summary(
        matrix_rows
    )

    print_high_maturity_technologies(
        matrix_rows
    )


if __name__ == "__main__":
    main()
    