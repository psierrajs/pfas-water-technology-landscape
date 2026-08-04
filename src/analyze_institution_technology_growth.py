from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/openalex_authorships.csv"
)

OUTPUT_DIR = Path(
    "data/processed/institution_technology_growth"
)

EARLY_YEARS = {
    2018,
    2019,
    2020,
    2021,
}

RECENT_YEARS = {
    2022,
    2023,
    2024,
    2025,
}

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


def build_growth_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Aggregate institution output by technology and period."""
    publication_sets: dict[
        tuple[str, str],
        dict[str, set[str]],
    ] = defaultdict(
        lambda: {
            "early": set(),
            "recent": set(),
            "all": set(),
        }
    )

    metadata: dict[
        str,
        tuple[str, str],
    ] = {}

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

        try:
            publication_year = int(
                row.get(
                    "publication_year",
                    "",
                )
            )
        except ValueError:
            continue

        openalex_id = row.get(
            "openalex_id",
            "",
        ).strip()

        if not openalex_id:
            continue

        technologies = split_technology_labels(
            row.get(
                "technology_labels",
                "",
            )
        )

        for technology in technologies:
            key = (
                institution_id,
                technology,
            )

            publication_sets[key]["all"].add(
                openalex_id
            )

            if publication_year in EARLY_YEARS:
                publication_sets[key]["early"].add(
                    openalex_id
                )

            if publication_year in RECENT_YEARS:
                publication_sets[key]["recent"].add(
                    openalex_id
                )

    output_rows: list[dict[str, Any]] = []

    for (
        institution_id,
        technology,
    ), periods in publication_sets.items():
        institution_name, country_code = metadata[
            institution_id
        ]

        early_count = len(periods["early"])
        recent_count = len(periods["recent"])
        total_count = len(periods["all"])

        absolute_growth = (
            recent_count - early_count
        )

        if early_count > 0:
            growth_ratio = (
                recent_count / early_count
            )
        elif recent_count > 0:
            growth_ratio = None
        else:
            growth_ratio = 0.0

        output_rows.append(
            {
                "institution_id": institution_id,
                "institution_name": institution_name,
                "country_code": country_code,
                "technology": technology,
                "early_publications": early_count,
                "recent_publications": recent_count,
                "absolute_growth": absolute_growth,
                "growth_ratio": growth_ratio,
                "total_primary_publications": total_count,
            }
        )

    return output_rows

def sort_growth_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort by recent output, growth, and total output."""
    return sorted(
        rows,
        key=lambda row: (
            row["recent_publications"],
            row["absolute_growth"],
            row["total_primary_publications"],
            row["institution_name"],
        ),
        reverse=True,
    )


def write_growth_csv(
    rows: list[dict[str, Any]],
) -> Path:
    """Write the institution-technology growth table."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        OUTPUT_DIR
        / "institution_technology_growth.csv"
    )

    fieldnames = [
        "institution_id",
        "institution_name",
        "country_code",
        "technology",
        "early_publications",
        "recent_publications",
        "absolute_growth",
        "growth_ratio",
        "total_primary_publications",
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


def print_top_growth(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print established momentum and emerging entrants."""
    established_rows = [
        row
        for row in rows
        if (
            row["early_publications"] >= 1
            and row["recent_publications"]
            > row["early_publications"]
        )
    ]

    established_rows = sorted(
        established_rows,
        key=lambda row: (
            row["absolute_growth"],
            row["recent_publications"],
            row["total_primary_publications"],
        ),
        reverse=True,
    )

    print(
        "\nEstablished institution–technology momentum"
    )
    print("-" * 120)

    for row in established_rows[:limit]:
        ratio = row["growth_ratio"]

        print(
            f"{row['recent_publications']:>3} recent | "
            f"{row['early_publications']:>3} early | "
            f"{row['absolute_growth']:>+3} change | "
            f"{ratio:>5.1f}x | "
            f"{row['institution_name']} "
            f"({row['country_code']}) | "
            f"{row['technology']}"
        )

    emerging_rows = [
        row
        for row in rows
        if (
            row["early_publications"] == 0
            and row["recent_publications"] >= 2
        )
    ]

    emerging_rows = sorted(
        emerging_rows,
        key=lambda row: (
            row["recent_publications"],
            row["total_primary_publications"],
            row["institution_name"],
        ),
        reverse=True,
    )

    print(
        "\nEmerging institution–technology entrants"
    )
    print("-" * 120)

    for row in emerging_rows[:limit]:
        print(
            f"{row['recent_publications']:>3} recent | "
            f"{row['total_primary_publications']:>3} total | "
            f"{row['institution_name']} "
            f"({row['country_code']}) | "
            f"{row['technology']}"
        )

def main() -> None:
    """Run the institution–technology growth analysis."""
    rows = read_authorship_rows()

    growth_rows = build_growth_rows(rows)
    growth_rows = sort_growth_rows(
        growth_rows
    )

    output_path = write_growth_csv(
        growth_rows
    )

    print(
        f"Authorship rows read: {len(rows)}"
    )
    print(
        "Institution–technology combinations: "
        f"{len(growth_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )

    print_top_growth(
        growth_rows
    )


if __name__ == "__main__":
    main()