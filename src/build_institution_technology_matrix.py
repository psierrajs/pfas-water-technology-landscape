from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/openalex_authorships.csv"
)

OUTPUT_DIR = Path(
    "data/processed/institution_technology_matrix"
)

PRIMARY_TIERS = {
    "core",
    "secondary",
    "manual_review",
}

INSTITUTION_ALIASES = {
    "https://openalex.org/I4210126337": (
        "https://openalex.org/I197809005"
    ),
    "https://openalex.org/I113508548": (
        "https://openalex.org/I392282"
    ),
    "https://openalex.org/I4210150356": (
        "https://openalex.org/I201448701"
    ),
    "https://openalex.org/I4405270011": (
        "https://openalex.org/I204337017"
    ),
}

CANONICAL_INSTITUTION_METADATA = {
    "https://openalex.org/I197809005": {
        "institution_name": (
            "University of Campania Luigi Vanvitelli"
        ),
        "institution_country_code": "IT",
    },
    "https://openalex.org/I392282": {
        "institution_name": (
            "University at Albany, SUNY"
        ),
        "institution_country_code": "US",
    },
    "https://openalex.org/I201448701": {
        "institution_name": (
            "University of Washington"
        ),
        "institution_country_code": "US",
    },
    "https://openalex.org/I204337017": {
        "institution_name": "Aarhus University",
        "institution_country_code": "DK",
    },
}

US_EPA_ID = "https://openalex.org/I1302368450"
GHANA_EPA_ID = "https://openalex.org/I182185646"

def canonical_institution_id(
    institution_id: str,
) -> str:
    """Return the canonical OpenAlex institution ID."""
    return INSTITUTION_ALIASES.get(
        institution_id,
        institution_id,
    )


def corrected_institution_id(
    row: dict[str, str],
) -> str:
    """Correct known affiliation-resolution errors."""
    institution_id = canonical_institution_id(
        row.get("institution_id", "").strip()
    )

    raw_affiliation = row.get(
        "raw_affiliations",
        "",
    ).casefold()

    us_epa_signals = (
        "u.s. environmental protection agency",
        "us environmental protection agency",
        "cincinnati, oh",
        "cincinnati ohio",
        "durham, nc",
    )

    if (
        institution_id == GHANA_EPA_ID
        and any(
            signal in raw_affiliation
            for signal in us_epa_signals
        )
    ):
        return US_EPA_ID

    return institution_id


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


def institution_metadata(
    row: dict[str, str],
    institution_id: str,
) -> tuple[str, str]:
    """Return normalized institution name and country."""
    canonical = CANONICAL_INSTITUTION_METADATA.get(
        institution_id
    )

    if canonical:
        return (
            canonical["institution_name"],
            canonical["institution_country_code"],
        )

    return (
        row.get("institution_name", "").strip(),
        row.get(
            "institution_country_code",
            "",
        ).strip(),
    )

def read_authorship_rows() -> list[dict[str, str]]:
    """Read the enriched authorship dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def build_matrix_rows(
    rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, Any]],
    list[str],
]:
    """Build one institution row with counts by technology."""
    publication_sets: dict[
        str,
        dict[str, set[str]],
    ] = defaultdict(
        lambda: defaultdict(set)
    )

    metadata: dict[
        str,
        tuple[str, str],
    ] = {}

    technologies: set[str] = set()

    for row in rows:
        tier = row.get(
            "analysis_tier",
            "",
        ).strip()

        if tier not in PRIMARY_TIERS:
            continue

        institution_id = corrected_institution_id(row)

        if not institution_id:
            continue

        institution_name, country_code = (
            institution_metadata(
                row,
                institution_id,
            )
        )

        metadata[institution_id] = (
            institution_name,
            country_code,
        )

        openalex_id = row.get(
            "openalex_id",
            "",
        ).strip()

        if not openalex_id:
            continue

        labels = split_technology_labels(
            row.get(
                "technology_labels",
                "",
            )
        )

        for technology in labels:
            technologies.add(technology)
            publication_sets[
                institution_id
            ][technology].add(openalex_id)

    technology_columns = sorted(technologies)
    matrix_rows: list[dict[str, Any]] = []

    for institution_id, technology_sets in (
        publication_sets.items()
    ):
        institution_name, country_code = metadata[
            institution_id
        ]

        row: dict[str, Any] = {
            "institution_id": institution_id,
            "institution_name": institution_name,
            "country_code": country_code,
        }

        total_publications: set[str] = set()
        active_technologies = 0
        supported_technologies = 0

        for technology in technology_columns:
            publications = technology_sets.get(
                technology,
                set(),
            )

            count = len(publications)
            row[technology] = count

            if count > 0:
                active_technologies += 1
                total_publications.update(publications)
            if count >= 2:
                supported_technologies += 1

        row["active_technology_count"] = (
            active_technologies
        )
        row["supported_technology_count"] = (
            supported_technologies
        )
        row["total_unique_publications"] = len(
            total_publications
        )

        matrix_rows.append(row)

    return (
        matrix_rows,
        technology_columns,
    )

def sort_matrix_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort institutions by breadth and publication volume."""
    return sorted(
        rows,
        key=lambda row: (
            row["supported_technology_count"],
            row["active_technology_count"],
            row["total_unique_publications"],
            row["institution_name"],
        ),
        reverse=True,
    )


def write_matrix_csv(
    rows: list[dict[str, Any]],
    technology_columns: list[str],
) -> Path:
    """Write the institution–technology matrix."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / "institution_technology_matrix.csv"
    )

    fieldnames = [
        "institution_id",
        "institution_name",
        "country_code",
        "active_technology_count",
        "supported_technology_count",
        "total_unique_publications",
        *technology_columns,
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


def print_broadest_institutions(
    rows: list[dict[str, Any]],
    technology_columns: list[str],
    limit: int = 20,
) -> None:
    """Print robust and low-volume technology breadth."""
    robust_rows = [
        row
        for row in rows
        if row["total_unique_publications"] >= 3
    ]

    robust_rows = sorted(
        robust_rows,
        key=lambda row: (
            row["supported_technology_count"],
            row["active_technology_count"],
            row["total_unique_publications"],
            row["institution_name"],
        ),
        reverse=True,
    )

    print(
        "\nInstitutions with robust technology breadth"
    )
    print("-" * 120)

    for row in robust_rows[:limit]:
        leading_technologies = sorted(
            (
                (
                    technology,
                    row[technology],
                )
                for technology in technology_columns
                if row[technology] > 0
            ),
            key=lambda item: (
                item[1],
                item[0],
            ),
            reverse=True,
        )

        technology_text = ", ".join(
            f"{technology}={count}"
            for technology, count
            in leading_technologies[:5]
        )

        print(
            f"{row['supported_technology_count']:>2} supported | "
            f"{row['active_technology_count']:>2} active | "
            f"{row['total_unique_publications']:>3} publications | "
            f"{row['institution_name']} "
            f"({row['country_code']}) | "
            f"{technology_text}"
        )

    low_volume_rows = [
        row
        for row in rows
        if (
            row["total_unique_publications"] < 3
            and row["active_technology_count"] >= 5
        )
    ]

    low_volume_rows = sorted(
        low_volume_rows,
        key=lambda row: (
            row["active_technology_count"],
            row["total_unique_publications"],
            row["institution_name"],
        ),
        reverse=True,
    )

    print(
        "\nHigh breadth based on fewer than three publications"
    )
    print("-" * 120)

    for row in low_volume_rows[:limit]:
        print(
            f"{row['supported_technology_count']:>2} supported | "
            f"{row['active_technology_count']:>2} active | "
            f"{row['total_unique_publications']:>3} publications | "
            f"{row['institution_name']} "
            f"({row['country_code']})"
        )

def main() -> None:
    """Build the institution–technology matrix."""
    rows = read_authorship_rows()

    matrix_rows, technology_columns = (
        build_matrix_rows(rows)
    )

    matrix_rows = sort_matrix_rows(
        matrix_rows
    )

    output_path = write_matrix_csv(
        matrix_rows,
        technology_columns,
    )

    print(
        f"Authorship rows read: {len(rows)}"
    )
    print(
        f"Institutions in matrix: {len(matrix_rows)}"
    )
    print(
        f"Technology columns: {len(technology_columns)}"
    )
    print(
        f"Output written to: {output_path}"
    )

    print_broadest_institutions(
        matrix_rows,
        technology_columns,
    )


if __name__ == "__main__":
    main()

