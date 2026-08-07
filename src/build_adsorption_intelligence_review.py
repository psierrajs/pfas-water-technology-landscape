from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_prefilled.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_review.csv"
)

INTELLIGENCE_FIELDS = (
    "treatment_mode",
    "carbon_type",
    "target_matrix",
    "pfas_handling",
    "system_configuration",
    "maturity_signal",
    "strategic_theme",
)

def read_rows() -> list[dict[str, str]]:
    """Read the prefilled family intelligence dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def uncertain_fields(
    row: dict[str, str],
) -> list[str]:
    """Return intelligence fields still classified as uncertain."""
    return [
        field
        for field in INTELLIGENCE_FIELDS
        if row.get(
            field,
            "",
        ).strip() == "uncertain"
    ]


def needs_review(
    row: dict[str, str],
) -> bool:
    """Return True when at least one intelligence field is uncertain."""
    return bool(
        uncertain_fields(row)
    )

def build_review_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Build a compact review table for uncertain family classifications."""
    review_rows: list[dict[str, str]] = []

    for row in rows:
        if not needs_review(row):
            continue

        updated_row = dict(row)

        fields = uncertain_fields(
            row
        )

        updated_row[
            "uncertain_field_count"
        ] = str(
            len(fields)
        )

        updated_row[
            "uncertain_fields"
        ] = "; ".join(
            fields
        )

        review_rows.append(
            updated_row
        )

    return sorted(
        review_rows,
        key=lambda row: (
            -int(
                row.get(
                    "uncertain_field_count",
                    "0",
                )
                or 0
            ),
            row.get(
                "family_group",
                "",
            ),
        ),
    )

def write_review_rows(
    rows: list[dict[str, str]],
) -> Path:
    """Write the uncertain family intelligence review dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No uncertain intelligence classifications were found."
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
    source_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
) -> None:
    """Print a short summary of the intelligence review dataset."""
    print(
        f"Included patent families: {len(source_rows)}"
    )

    print(
        f"Families needing intelligence review: {len(review_rows)}"
    )

    uncertainty_counts: dict[str, int] = {}

    for row in review_rows:
        fields = uncertain_fields(
            row
        )

        for field in fields:
            uncertainty_counts[field] = (
                uncertainty_counts.get(field, 0) + 1
            )

    for field in INTELLIGENCE_FIELDS:
        if field in uncertainty_counts:
            print(
                f"{field}: {uncertainty_counts[field]}"
            )


def main() -> None:
    """Build the uncertain family intelligence review dataset."""
    source_rows = read_rows()

    review_rows = build_review_rows(
        source_rows
    )

    output_path = write_review_rows(
        review_rows
    )

    print_summary(
        source_rows,
        review_rows,
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
