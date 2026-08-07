from __future__ import annotations

import csv
from pathlib import Path


BASELINE_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_prefilled.csv"
)

REVIEWED_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_review_prefilled.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_final.csv"
)

def read_csv_rows(
    path: Path,
) -> list[dict[str, str]]:
    """Read all rows from a CSV file."""
    with path.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def index_rows_by_family(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, str]]:
    """Index rows by family_group."""
    indexed: dict[str, dict[str, str]] = {}

    for row in rows:
        family_group = row.get(
            "family_group",
            "",
        ).strip()

        if not family_group:
            continue

        indexed[family_group] = row

    return indexed

INTELLIGENCE_FIELDS = (
    "treatment_mode",
    "carbon_type",
    "target_matrix",
    "pfas_handling",
    "system_configuration",
    "maturity_signal",
    "strategic_theme",
    "intelligence_notes",
)


def merge_reviewed_rows(
    baseline_rows: list[dict[str, str]],
    reviewed_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Replace baseline intelligence fields with reviewed values."""
    reviewed_by_family = index_rows_by_family(
        reviewed_rows
    )

    output_rows: list[dict[str, str]] = []

    for row in baseline_rows:
        updated_row = dict(row)

        family_group = row.get(
            "family_group",
            "",
        ).strip()

        reviewed_row = reviewed_by_family.get(
            family_group
        )

        if reviewed_row:
            for field in INTELLIGENCE_FIELDS:
                reviewed_value = reviewed_row.get(
                    field,
                    "",
                ).strip()

                if reviewed_value:
                    updated_row[field] = reviewed_value

        output_rows.append(
            updated_row
        )

    return output_rows

def validate_final_rows(
    rows: list[dict[str, str]],
) -> None:
    """Validate that all final intelligence fields are populated."""
    problems: list[str] = []

    for row in rows:
        family_group = row.get(
            "family_group",
            "",
        ).strip()

        for field in INTELLIGENCE_FIELDS[:-1]:
            value = row.get(
                field,
                "",
            ).strip()

            if not value or value == "uncertain":
                problems.append(
                    f"{family_group}: {field}={value or 'blank'}"
                )

    if problems:
        problem_text = "\n".join(
            problems
        )

        raise ValueError(
            "Unresolved intelligence fields remain:\n"
            f"{problem_text}"
        )


def write_final_rows(
    rows: list[dict[str, str]],
) -> Path:
    """Write the final family intelligence dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No family intelligence records were found."
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
    """Print a compact summary of the final intelligence dataset."""
    print(
        f"Final patent families: {len(rows)}"
    )

    for field in INTELLIGENCE_FIELDS[:-1]:
        counts: dict[str, int] = {}

        for row in rows:
            value = row.get(
                field,
                "",
            ).strip() or "blank"

            counts[value] = (
                counts.get(value, 0) + 1
            )

        print(f"\n{field}:")

        for value, count in sorted(
            counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        ):
            print(
                f"  {value}: {count}"
            )


def main() -> None:
    """Build the final family-level intelligence dataset."""
    baseline_rows = read_csv_rows(
        BASELINE_PATH
    )

    reviewed_rows = read_csv_rows(
        REVIEWED_PATH
    )

    final_rows = merge_reviewed_rows(
        baseline_rows,
        reviewed_rows,
    )

    validate_final_rows(
        final_rows
    )

    output_path = write_final_rows(
        final_rows
    )

    print_summary(
        final_rows
    )

    print(
        f"\nOutput written to: {output_path}"
    )


if __name__ == "__main__":
    main()

