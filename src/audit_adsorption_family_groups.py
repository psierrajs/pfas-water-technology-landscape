from __future__ import annotations

import csv
from collections import Counter
from datetime import date
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening_corrected.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_audit.csv"
)


TITLE_SIMILARITY_THRESHOLD = 0.45
PRIORITY_DATE_GAP_YEARS = 5

VALIDATED_FAMILIES = {
    "FAM-ADS-034": (
        "Manually validated as one family. The English and Chinese "
        "assignee names both refer to Taiwan Semiconductor "
        "Manufacturing Company, and title differences reflect "
        "translation or jurisdiction-specific wording."
    ),
}

def read_screening_rows() -> list[dict[str, str]]:
    """Read the consolidated adsorption screening dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalize_title(
    title: str,
) -> set[str]:
    """Convert a title into a set of normalized words."""
    normalized = (
        title.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
    )

    return {
        word
        for word in normalized.split()
        if len(word) > 2
    }


def title_similarity(
    first_title: str,
    second_title: str,
) -> float:
    """Calculate Jaccard similarity between two titles."""
    first_words = normalize_title(
        first_title
    )

    second_words = normalize_title(
        second_title
    )

    if not first_words or not second_words:
        return 0.0

    intersection = first_words & second_words
    union = first_words | second_words

    return len(intersection) / len(union)


def parse_priority_date(
    value: str,
) -> date | None:
    """Parse an ISO-formatted priority date."""
    value = value.strip()

    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def group_rows_by_family(
    rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Group screening records by provisional family ID."""
    families: dict[str, list[dict[str, str]]] = {}

    for row in rows:
        family_group = row.get(
            "manual_family_group",
            "",
        ).strip()

        if not family_group:
            continue

        families.setdefault(
            family_group,
            [],
        ).append(row)

    return families


def minimum_title_similarity(
    rows: list[dict[str, str]],
) -> float:
    """Return the lowest pairwise title similarity in a family."""
    titles = [
        row.get(
            "title",
            "",
        ).strip()
        for row in rows
        if row.get(
            "title",
            "",
        ).strip()
    ]

    if len(titles) < 2:
        return 1.0

    similarities: list[float] = []

    for index, first_title in enumerate(titles):
        for second_title in titles[index + 1:]:
            similarities.append(
                title_similarity(
                    first_title,
                    second_title,
                )
            )

    return min(similarities) if similarities else 1.0

def priority_date_gap_years(
    rows: list[dict[str, str]],
) -> float:
    """Return the span between the earliest and latest priority dates."""
    dates = [
        parsed_date
        for row in rows
        if (
            parsed_date := parse_priority_date(
                row.get(
                    "priority_date",
                    "",
                )
            )
        )
        is not None
    ]

    if len(dates) < 2:
        return 0.0

    earliest = min(dates)
    latest = max(dates)

    return (
        latest - earliest
    ).days / 365.25


def collect_distinct_values(
    rows: list[dict[str, str]],
    field: str,
) -> list[str]:
    """Collect sorted non-empty distinct values from a field."""
    return sorted(
        {
            row.get(
                field,
                "",
            ).strip()
            for row in rows
            if row.get(
                field,
                "",
            ).strip()
        }
    )


def extract_jurisdictions(
    rows: list[dict[str, str]],
) -> list[str]:
    """Extract publication jurisdiction prefixes."""
    jurisdictions = {
        row.get(
            "publication_id",
            "",
        ).split(
            "-",
            maxsplit=1,
        )[0]
        for row in rows
        if row.get(
            "publication_id",
            "",
        ).strip()
    }

    return sorted(
        jurisdiction
        for jurisdiction in jurisdictions
        if jurisdiction
    )

def build_audit_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build one audit row per provisional patent family."""
    families = group_rows_by_family(
        rows
    )

    audit_rows: list[dict[str, str]] = []

    for family_group, family_rows in families.items():
        publication_ids = collect_distinct_values(
            family_rows,
            "publication_id",
        )

        titles = collect_distinct_values(
            family_rows,
            "title",
        )

        assignees = collect_distinct_values(
            family_rows,
            "assignee_original",
        )

        decisions = collect_distinct_values(
            family_rows,
            "manual_relevance_decision",
        )

        similarity = minimum_title_similarity(
            family_rows
        )

        date_gap = priority_date_gap_years(
            family_rows
        )

        flags: list[str] = []

        if (
            len(family_rows) > 1
            and similarity < TITLE_SIMILARITY_THRESHOLD
        ):
            flags.append(
                "low_title_similarity"
            )

        if (
            len(family_rows) > 1
            and len(assignees) > 1
        ):
            flags.append(
                "multiple_assignees"
            )

        if date_gap > PRIORITY_DATE_GAP_YEARS:
            flags.append(
                "large_priority_date_gap"
            )

        if len(decisions) > 1:
            flags.append(
                "conflicting_decisions"
            )
        validation_note = VALIDATED_FAMILIES.get(
            family_group,
            "",
        )

        needs_review = bool(
            flags
            and not validation_note
        )
        audit_rows.append(
            {
                "family_group": family_group,
                "publication_count": str(
                    len(publication_ids)
                ),
                "publication_ids": "; ".join(
                    publication_ids
                ),
                "jurisdictions": "; ".join(
                    extract_jurisdictions(
                        family_rows
                    )
                ),
                "title_count": str(
                    len(titles)
                ),
                "minimum_title_similarity": (
                    f"{similarity:.3f}"
                ),
                "assignee_count": str(
                    len(assignees)
                ),
                "assignees": "; ".join(
                    assignees
                ),
                "priority_date_gap_years": (
                    f"{date_gap:.1f}"
                ),
                "decisions": "; ".join(
                    decisions
                ),
                "audit_flags": "; ".join(
                    flags
                ),
                "validation_note": validation_note,
                "needs_review": (
                    "yes"
                    if needs_review
                    else "no"
                ),
            }
        )

    return sorted(
        audit_rows,
        key=lambda row: (
            row["needs_review"] != "yes",
            row["family_group"],
        ),
    )

def write_audit_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the provisional family-group audit."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No provisional patent families were found."
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
    rows: list[dict[str, str]],
) -> None:
    """Print a short audit summary."""
    review_rows = [
        row
        for row in rows
        if row.get(
            "needs_review",
            "",
        ) == "yes"
    ]

    flag_counts: Counter[str] = Counter()

    for row in review_rows:
        for flag in row.get(
            "audit_flags",
            "",
        ).split(";"):
            flag = flag.strip()

            if flag:
                flag_counts[flag] += 1

    print(
        f"Provisional families audited: {len(rows)}"
    )
    print(
        f"Families needing review: {len(review_rows)}"
    )

    for flag, count in flag_counts.most_common():
        print(
            f"{flag}: {count}"
        )


def main() -> None:
    """Audit provisional adsorption family assignments."""
    source_rows = read_screening_rows()

    audit_rows = build_audit_rows(
        source_rows
    )

    output_path = write_audit_csv(
        audit_rows
    )

    print_summary(
        audit_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
