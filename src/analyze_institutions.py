from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path(
    "data/processed/openalex_authorships.csv"
)

DEFAULT_OUTPUT_DIR = Path(
    "data/processed/institutions"
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
}

CANONICAL_INSTITUTION_METADATA = {
    "https://openalex.org/I197809005": {
        "institution_name": (
            'University of Campania "Luigi Vanvitelli"'
        ),
        "country_code": "IT",
        "institution_type": "education",
        "institution_ror": "https://ror.org/02kqnpp86",
    },
    "https://openalex.org/I392282": {
        "institution_name": (
            "University at Albany, "
            "State University of New York"
        ),
        "country_code": "US",
        "institution_type": "education",
        "institution_ror": "",
    },
    "https://openalex.org/I201448701": {
        "institution_name": "University of Washington",
        "country_code": "US",
        "institution_type": "education",
        "institution_ror": "",
    },
}

US_EPA_ID = "https://openalex.org/I1302368450"
GHANA_EPA_ID = "https://openalex.org/I182185646"

def read_csv(path: Path) -> list[dict[str, str]]:
    """Read the enriched authorship dataset."""
    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def parse_labels(value: str) -> set[str]:
    """Parse semicolon-delimited technology labels."""
    return {
        label.strip()
        for label in value.split(";")
        if label.strip()
    }


def valid_institution(row: dict[str, str]) -> bool:
    """Return whether the row contains an institution."""
    return bool(
        row.get("institution_id", "").strip()
        and row.get("institution_name", "").strip()
    )

def canonical_institution_id(
    institution_id: str,
) -> str:
    """Map known duplicate institution IDs to canonical IDs."""
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

def deduplicate_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """
    Deduplicate repeated work-author-institution records.

    OpenAlex occasionally returns duplicate affiliation mappings.
    """
    deduplicated: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    for row in rows:
        key = (
            row.get("openalex_id", "").strip(),
            row.get("author_id", "").strip(),
            row.get("institution_id", "").strip(),
        )

        if key in seen:
            continue

        seen.add(key)
        deduplicated.append(row)

    return deduplicated


def institution_metadata(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    """Collect stable metadata for each institution."""
    metadata: dict[str, dict[str, str]] = {}

    for row in rows:
        if not valid_institution(row):
            continue

        institution_id = corrected_institution_id(row)

        if institution_id not in metadata:
            metadata[institution_id] = {
                "institution_id": institution_id,
                "institution_name": row[
                    "institution_name"
                ].strip(),
                "institution_ror": row.get(
                    "institution_ror",
                    "",
                ).strip(),
                "country_code": row.get(
                    "institution_country_code",
                    "",
                ).strip(),
                "institution_type": row.get(
                    "institution_type",
                    "",
                ).strip(),
            }
        elif (
            not metadata[institution_id]["institution_ror"]
            and row.get("institution_ror", "").strip()
        ):
            metadata[institution_id]["institution_ror"] = (
                row["institution_ror"].strip()
            )
    for institution_id, canonical_info in (
        CANONICAL_INSTITUTION_METADATA.items()
    ):
        if institution_id not in metadata:
            continue

        metadata[institution_id].update(
            canonical_info
        )
    return metadata

def build_institution_work_sets(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, set[str]]]:
    """Collect unique works for each institution."""
    work_sets: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {
            "all": set(),
            "primary": set(),
            "core": set(),
            "secondary": set(),
            "manual_review": set(),
            "background": set(),
            "exclude_candidate": set(),
        }
    )

    for row in rows:
        if not valid_institution(row):
            continue

        institution_id = corrected_institution_id(row)
        work_id = row.get("openalex_id", "").strip()
        tier = row.get("analysis_tier", "").strip()

        if not work_id:
            continue

        work_sets[institution_id]["all"].add(work_id)

        if tier in PRIMARY_TIERS:
            work_sets[institution_id]["primary"].add(work_id)

        if tier in work_sets[institution_id]:
            work_sets[institution_id][tier].add(work_id)

    return work_sets

def build_institution_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Build publication counts for each institution."""
    metadata = institution_metadata(rows)
    work_sets = build_institution_work_sets(rows)

    summary: list[dict[str, Any]] = []

    for institution_id, tier_sets in work_sets.items():
        info = metadata[institution_id]

        all_count = len(tier_sets["all"])
        primary_count = len(tier_sets["primary"])
        core_count = len(tier_sets["core"])

        summary.append(
            {
                **info,
                "all_publications": all_count,
                "primary_publications": primary_count,
                "core_publications": core_count,
                "secondary_publications": len(
                    tier_sets["secondary"]
                ),
                "manual_review_publications": len(
                    tier_sets["manual_review"]
                ),
                "background_publications": len(
                    tier_sets["background"]
                ),
                "exclude_candidate_publications": len(
                    tier_sets["exclude_candidate"]
                ),
                "core_share_of_all": (
                    f"{core_count / all_count:.4f}"
                    if all_count
                    else "0.0000"
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["core_publications"]),
            -int(row["primary_publications"]),
            -int(row["all_publications"]),
            str(row["institution_name"]),
        )
    )

    return summary


def build_country_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Count unique works associated with each country."""
    country_work_sets: dict[
        str,
        dict[str, set[str]],
    ] = defaultdict(
        lambda: {
            "all": set(),
            "primary": set(),
            "core": set(),
        }
    )

    for row in rows:
        if not valid_institution(row):
            continue

        country_code = row.get(
            "institution_country_code",
            "",
        ).strip()
        work_id = row.get("openalex_id", "").strip()
        tier = row.get("analysis_tier", "").strip()

        if not country_code or not work_id:
            continue

        country_work_sets[country_code]["all"].add(
            work_id
        )

        if tier in PRIMARY_TIERS:
            country_work_sets[country_code][
                "primary"
            ].add(work_id)

        if tier == "core":
            country_work_sets[country_code][
                "core"
            ].add(work_id)

    summary = []

    for country_code, work_sets in country_work_sets.items():
        summary.append(
            {
                "country_code": country_code,
                "all_publications": len(
                    work_sets["all"]
                ),
                "primary_publications": len(
                    work_sets["primary"]
                ),
                "core_publications": len(
                    work_sets["core"]
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["core_publications"]),
            -int(row["primary_publications"]),
            -int(row["all_publications"]),
            str(row["country_code"]),
        )
    )

    return summary


def build_institution_technology_summary(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Count unique works by institution and technology."""
    counts: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    metadata = institution_metadata(rows)

    for row in rows:
        if not valid_institution(row):
            continue

        tier = row.get("analysis_tier", "").strip()

        if tier not in PRIMARY_TIERS:
            continue

        institution_id = corrected_institution_id(row)
        work_id = row.get("openalex_id", "").strip()

        for technology in parse_labels(
            row.get("technology_labels", "")
        ):
            counts[
                (institution_id, technology)
            ].add(work_id)

    summary = []

    for (
        institution_id,
        technology,
    ), work_ids in counts.items():
        info = metadata[institution_id]

        summary.append(
            {
                **info,
                "technology_label": technology,
                "publication_count": len(work_ids),
            }
        )

    summary.sort(
        key=lambda row: (
            str(row["technology_label"]),
            -int(row["publication_count"]),
            str(row["institution_name"]),
        )
    )

    return summary

def write_csv(
    rows: list[dict[str, Any]],
    path: Path,
    fieldnames: list[str],
) -> None:
    """Write analysis rows to CSV."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
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


def print_top_institutions(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print the highest-ranked institutions."""
    print("\nTop institutions by core publications")
    print("-" * 88)

    print(
        "Institution".ljust(48)
        + "Country".rjust(10)
        + "Core".rjust(8)
        + "Primary".rjust(10)
        + "All".rjust(8)
    )

    for row in rows[:limit]:
        print(
            str(row["institution_name"])[:47].ljust(48)
            + str(row["country_code"]).rjust(10)
            + str(row["core_publications"]).rjust(8)
            + str(row["primary_publications"]).rjust(10)
            + str(row["all_publications"]).rjust(8)
        )


def print_top_countries(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print the highest-ranked countries."""
    print("\nTop countries by core publications")
    print("-" * 56)

    print(
        "Country".ljust(12)
        + "Core".rjust(10)
        + "Primary".rjust(12)
        + "All".rjust(10)
    )

    for row in rows[:limit]:
        print(
            str(row["country_code"]).ljust(12)
            + str(row["core_publications"]).rjust(10)
            + str(row["primary_publications"]).rjust(12)
            + str(row["all_publications"]).rjust(10)
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze institutions and countries in the "
            "PFAS water-treatment literature corpus."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    deduplicated_rows = deduplicate_rows(rows)

    institution_summary = build_institution_summary(
        deduplicated_rows
    )
    country_summary = build_country_summary(
        deduplicated_rows
    )
    institution_technology_summary = (
        build_institution_technology_summary(
            deduplicated_rows
        )
    )

    write_csv(
        institution_summary,
        args.output_dir / "institution_summary.csv",
        [
            "institution_id",
            "institution_name",
            "institution_ror",
            "country_code",
            "institution_type",
            "all_publications",
            "primary_publications",
            "core_publications",
            "secondary_publications",
            "manual_review_publications",
            "background_publications",
            "exclude_candidate_publications",
            "core_share_of_all",
        ],
    )

    write_csv(
        country_summary,
        args.output_dir / "country_summary.csv",
        [
            "country_code",
            "all_publications",
            "primary_publications",
            "core_publications",
        ],
    )

    write_csv(
        institution_technology_summary,
        args.output_dir
        / "institution_technology_summary.csv",
        [
            "institution_id",
            "institution_name",
            "institution_ror",
            "country_code",
            "institution_type",
            "technology_label",
            "publication_count",
        ],
    )

    print(
        f"Authorship rows read: {len(rows)}"
    )
    print(
        "Rows after work-author-institution "
        f"deduplication: {len(deduplicated_rows)}"
    )
    print(
        f"Institutions analysed: "
        f"{len(institution_summary)}"
    )
    print(
        f"Countries analysed: {len(country_summary)}"
    )

    print_top_institutions(institution_summary)
    print_top_countries(country_summary)

    print(
        f"\nSaved outputs to: {args.output_dir}"
    )


if __name__ == "__main__":
    main()