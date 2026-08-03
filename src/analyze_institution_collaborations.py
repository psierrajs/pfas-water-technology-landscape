from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path(
    "data/processed/openalex_authorships.csv"
)

DEFAULT_OUTPUT_DIR = Path(
    "data/processed/institution_collaborations"
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

def valid_institution(row: dict[str, str]) -> bool:
    """Return whether the row contains an institution."""
    return bool(
        row.get("institution_id", "").strip()
        and row.get("institution_name", "").strip()
    )


def parse_labels(value: str) -> set[str]:
    """Parse semicolon-delimited technology labels."""
    return {
        label.strip()
        for label in value.split(";")
        if label.strip()
    }


def institution_metadata(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    """Collect metadata for canonical institution IDs."""
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
                "country_code": row.get(
                    "institution_country_code",
                    "",
                ).strip(),
                "institution_type": row.get(
                    "institution_type",
                    "",
                ).strip(),
                "institution_ror": row.get(
                    "institution_ror",
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

def build_work_records(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    """Collect institutions and metadata for each work."""
    works: dict[str, dict[str, Any]] = {}

    for row in rows:
        work_id = row.get("openalex_id", "").strip()

        if not work_id:
            continue

        if work_id not in works:
            works[work_id] = {
                "openalex_id": work_id,
                "title": row.get("title", "").strip(),
                "publication_year": row.get(
                    "publication_year",
                    "",
                ).strip(),
                "analysis_tier": row.get(
                    "analysis_tier",
                    "",
                ).strip(),
                "technology_labels": parse_labels(
                    row.get("technology_labels", "")
                ),
                "institution_ids": set(),
            }

        if valid_institution(row):
            institution_id = corrected_institution_id(row)
            works[work_id]["institution_ids"].add(
                institution_id
            )

    return works


def pair_key(
    institution_a: str,
    institution_b: str,
) -> tuple[str, str]:
    """Return a stable institution-pair key."""
    return tuple(
        sorted(
            (
                institution_a,
                institution_b,
            )
        )
    )


def build_collaboration_summary(
    works: dict[str, dict[str, Any]],
    metadata: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    """Count unique collaborating institution pairs."""
    pair_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    pair_core_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    pair_primary_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    for work_id, work in works.items():
        institution_ids = sorted(
            work["institution_ids"]
        )

        for institution_a, institution_b in combinations(
            institution_ids,
            2,
        ):
            key = pair_key(
                institution_a,
                institution_b,
            )
            pair_works[key].add(work_id)

            tier = work["analysis_tier"]

            if tier == "core":
                pair_core_works[key].add(work_id)

            if tier in PRIMARY_TIERS:
                pair_primary_works[key].add(work_id)

    summary: list[dict[str, Any]] = []

    for (
        institution_a,
        institution_b,
    ), work_ids in pair_works.items():
        info_a = metadata[institution_a]
        info_b = metadata[institution_b]

        country_a = info_a["country_code"]
        country_b = info_b["country_code"]

        summary.append(
            {
                "institution_a_id": institution_a,
                "institution_a_name": info_a[
                    "institution_name"
                ],
                "institution_a_country": country_a,
                "institution_a_type": info_a[
                    "institution_type"
                ],
                "institution_b_id": institution_b,
                "institution_b_name": info_b[
                    "institution_name"
                ],
                "institution_b_country": country_b,
                "institution_b_type": info_b[
                    "institution_type"
                ],
                "all_shared_publications": len(work_ids),
                "primary_shared_publications": len(
                    pair_primary_works[
                        (
                            institution_a,
                            institution_b,
                        )
                    ]
                ),
                "core_shared_publications": len(
                    pair_core_works[
                        (
                            institution_a,
                            institution_b,
                        )
                    ]
                ),
                "cross_country": (
                    "yes"
                    if (
                        country_a
                        and country_b
                        and country_a != country_b
                    )
                    else "no"
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["core_shared_publications"]),
            -int(row["primary_shared_publications"]),
            -int(row["all_shared_publications"]),
            str(row["institution_a_name"]),
            str(row["institution_b_name"]),
        )
    )

    return summary

def build_institution_network_summary(
    collaboration_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Summarize each institution's collaboration activity."""
    collaborators: dict[str, set[str]] = defaultdict(set)
    core_collaborators: dict[str, set[str]] = defaultdict(set)
    primary_collaborators: dict[str, set[str]] = defaultdict(set)

    shared_publications: Counter[str] = Counter()
    core_shared_publications: Counter[str] = Counter()
    primary_shared_publications: Counter[str] = Counter()
    cross_country_links: Counter[str] = Counter()

    metadata: dict[str, dict[str, str]] = {}

    for row in collaboration_rows:
        institution_a = str(row["institution_a_id"])
        institution_b = str(row["institution_b_id"])

        metadata[institution_a] = {
            "institution_name": str(
                row["institution_a_name"]
            ),
            "country_code": str(
                row["institution_a_country"]
            ),
            "institution_type": str(
                row["institution_a_type"]
            ),
        }
        metadata[institution_b] = {
            "institution_name": str(
                row["institution_b_name"]
            ),
            "country_code": str(
                row["institution_b_country"]
            ),
            "institution_type": str(
                row["institution_b_type"]
            ),
        }

        collaborators[institution_a].add(institution_b)
        collaborators[institution_b].add(institution_a)

        all_count = int(row["all_shared_publications"])
        primary_count = int(
            row["primary_shared_publications"]
        )
        core_count = int(row["core_shared_publications"])

        shared_publications[institution_a] += all_count
        shared_publications[institution_b] += all_count

        primary_shared_publications[
            institution_a
        ] += primary_count
        primary_shared_publications[
            institution_b
        ] += primary_count

        core_shared_publications[
            institution_a
        ] += core_count
        core_shared_publications[
            institution_b
        ] += core_count

        if primary_count > 0:
            primary_collaborators[institution_a].add(
                institution_b
            )
            primary_collaborators[institution_b].add(
                institution_a
            )

        if core_count > 0:
            core_collaborators[institution_a].add(
                institution_b
            )
            core_collaborators[institution_b].add(
                institution_a
            )

        if row["cross_country"] == "yes":
            cross_country_links[institution_a] += 1
            cross_country_links[institution_b] += 1

    summary: list[dict[str, Any]] = []

    for institution_id, info in metadata.items():
        summary.append(
            {
                "institution_id": institution_id,
                "institution_name": info[
                    "institution_name"
                ],
                "country_code": info["country_code"],
                "institution_type": info[
                    "institution_type"
                ],
                "all_collaborating_institutions": len(
                    collaborators[institution_id]
                ),
                "primary_collaborating_institutions": len(
                    primary_collaborators[
                        institution_id
                    ]
                ),
                "core_collaborating_institutions": len(
                    core_collaborators[
                        institution_id
                    ]
                ),
                "all_shared_publication_links": (
                    shared_publications[
                        institution_id
                    ]
                ),
                "primary_shared_publication_links": (
                    primary_shared_publications[
                        institution_id
                    ]
                ),
                "core_shared_publication_links": (
                    core_shared_publications[
                        institution_id
                    ]
                ),
                "cross_country_links": (
                    cross_country_links[
                        institution_id
                    ]
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["core_collaborating_institutions"]),
            -int(row["core_shared_publication_links"]),
            -int(
                row["primary_collaborating_institutions"]
            ),
            str(row["institution_name"]),
        )
    )

    return summary


def build_country_collaboration_summary(
    works: dict[str, dict[str, Any]],
    metadata: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    """Count country pairs represented on the same work."""
    pair_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    pair_core_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    pair_primary_works: dict[
        tuple[str, str],
        set[str],
    ] = defaultdict(set)

    for work_id, work in works.items():
        countries = sorted(
            {
                metadata[institution_id]["country_code"]
                for institution_id in work[
                    "institution_ids"
                ]
                if (
                    institution_id in metadata
                    and metadata[institution_id][
                        "country_code"
                    ]
                )
            }
        )

        for country_a, country_b in combinations(
            countries,
            2,
        ):
            key = (country_a, country_b)
            pair_works[key].add(work_id)

            tier = work["analysis_tier"]

            if tier == "core":
                pair_core_works[key].add(work_id)

            if tier in PRIMARY_TIERS:
                pair_primary_works[key].add(work_id)

    summary = []

    for (
        country_a,
        country_b,
    ), work_ids in pair_works.items():
        summary.append(
            {
                "country_a": country_a,
                "country_b": country_b,
                "all_shared_publications": len(work_ids),
                "primary_shared_publications": len(
                    pair_primary_works[
                        (country_a, country_b)
                    ]
                ),
                "core_shared_publications": len(
                    pair_core_works[
                        (country_a, country_b)
                    ]
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            -int(row["core_shared_publications"]),
            -int(row["primary_shared_publications"]),
            -int(row["all_shared_publications"]),
            str(row["country_a"]),
            str(row["country_b"]),
        )
    )

    return summary

def build_technology_collaboration_summary(
    works: dict[str, dict[str, Any]],
    metadata: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    """Count institution pairs within each technology."""
    pair_works: dict[
        tuple[str, str, str],
        set[str],
    ] = defaultdict(set)

    pair_core_works: dict[
        tuple[str, str, str],
        set[str],
    ] = defaultdict(set)

    for work_id, work in works.items():
        institution_ids = sorted(
            work["institution_ids"]
        )

        if len(institution_ids) < 2:
            continue

        for technology in work["technology_labels"]:
            for institution_a, institution_b in combinations(
                institution_ids,
                2,
            ):
                key = (
                    technology,
                    institution_a,
                    institution_b,
                )
                pair_works[key].add(work_id)

                if work["analysis_tier"] == "core":
                    pair_core_works[key].add(work_id)

    summary: list[dict[str, Any]] = []

    for (
        technology,
        institution_a,
        institution_b,
    ), work_ids in pair_works.items():
        info_a = metadata[institution_a]
        info_b = metadata[institution_b]

        summary.append(
            {
                "technology_label": technology,
                "institution_a_id": institution_a,
                "institution_a_name": info_a[
                    "institution_name"
                ],
                "institution_a_country": info_a[
                    "country_code"
                ],
                "institution_b_id": institution_b,
                "institution_b_name": info_b[
                    "institution_name"
                ],
                "institution_b_country": info_b[
                    "country_code"
                ],
                "all_shared_publications": len(work_ids),
                "core_shared_publications": len(
                    pair_core_works[
                        (
                            technology,
                            institution_a,
                            institution_b,
                        )
                    ]
                ),
            }
        )

    summary.sort(
        key=lambda row: (
            str(row["technology_label"]),
            -int(row["core_shared_publications"]),
            -int(row["all_shared_publications"]),
            str(row["institution_a_name"]),
            str(row["institution_b_name"]),
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


def print_top_collaborations(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print the strongest institutional pairs."""
    print("\nTop institutional collaborations")
    print("-" * 110)

    for row in rows[:limit]:
        print(
            f"{row['core_shared_publications']:>3} core | "
            f"{row['primary_shared_publications']:>3} primary | "
            f"{row['institution_a_name']} "
            f"({row['institution_a_country']})"
            " <-> "
            f"{row['institution_b_name']} "
            f"({row['institution_b_country']})"
        )


def print_top_network_institutions(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print institutions with the broadest core networks."""
    print("\nInstitutions with broadest core collaboration networks")
    print("-" * 100)

    for row in rows[:limit]:
        print(
            f"{row['core_collaborating_institutions']:>3} partners | "
            f"{row['core_shared_publication_links']:>3} links | "
            f"{row['institution_name']} "
            f"({row['country_code']})"
        )


def print_top_country_pairs(
    rows: list[dict[str, Any]],
    limit: int = 20,
) -> None:
    """Print leading international country pairs."""
    print("\nTop country collaborations")
    print("-" * 60)

    for row in rows[:limit]:
        print(
            f"{row['core_shared_publications']:>3} core | "
            f"{row['primary_shared_publications']:>3} primary | "
            f"{row['country_a']} <-> {row['country_b']}"
        )
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze institutional collaboration networks "
            "in the PFAS water-treatment literature."
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
    metadata = institution_metadata(rows)
    works = build_work_records(rows)

    collaboration_summary = build_collaboration_summary(
        works,
        metadata,
    )
    network_summary = build_institution_network_summary(
        collaboration_summary
    )
    country_summary = build_country_collaboration_summary(
        works,
        metadata,
    )
    technology_summary = (
        build_technology_collaboration_summary(
            works,
            metadata,
        )
    )

    write_csv(
        collaboration_summary,
        args.output_dir
        / "institution_collaboration_summary.csv",
        [
            "institution_a_id",
            "institution_a_name",
            "institution_a_country",
            "institution_a_type",
            "institution_b_id",
            "institution_b_name",
            "institution_b_country",
            "institution_b_type",
            "all_shared_publications",
            "primary_shared_publications",
            "core_shared_publications",
            "cross_country",
        ],
    )

    write_csv(
        network_summary,
        args.output_dir
        / "institution_network_summary.csv",
        [
            "institution_id",
            "institution_name",
            "country_code",
            "institution_type",
            "all_collaborating_institutions",
            "primary_collaborating_institutions",
            "core_collaborating_institutions",
            "all_shared_publication_links",
            "primary_shared_publication_links",
            "core_shared_publication_links",
            "cross_country_links",
        ],
    )

    write_csv(
        country_summary,
        args.output_dir
        / "country_collaboration_summary.csv",
        [
            "country_a",
            "country_b",
            "all_shared_publications",
            "primary_shared_publications",
            "core_shared_publications",
        ],
    )

    write_csv(
        technology_summary,
        args.output_dir
        / "technology_collaboration_summary.csv",
        [
            "technology_label",
            "institution_a_id",
            "institution_a_name",
            "institution_a_country",
            "institution_b_id",
            "institution_b_name",
            "institution_b_country",
            "all_shared_publications",
            "core_shared_publications",
        ],
    )

    print(f"Authorship rows read: {len(rows)}")
    print(f"Works analyzed: {len(works)}")
    print(
        "Institution pairs identified: "
        f"{len(collaboration_summary)}"
    )
    print(
        "Institutions in collaboration network: "
        f"{len(network_summary)}"
    )
    print(
        "Country pairs identified: "
        f"{len(country_summary)}"
    )

    print_top_collaborations(
        collaboration_summary
    )
    print_top_network_institutions(
        network_summary
    )
    print_top_country_pairs(
        country_summary
    )

    print(
        f"\nSaved outputs to: {args.output_dir}"
    )


if __name__ == "__main__":
    main()