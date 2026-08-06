from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_consolidated_screening_corrected.csv"
)


FAMILY_CORRECTIONS = {
    "WO-2026019974-A1": "FAM-ADS-046",
    "AU-2017371390-A1": "FAM-ADS-042",
    "CN-104773884-A": "FAM-ADS-043",
    "CN-121698443-A": "FAM-ADS-044",
    "GR-1006855-B": "FAM-ADS-045",
    "GR-20060100233-A": "FAM-ADS-045",
}

def read_rows() -> list[dict[str, str]]:
    """Read the consolidated adsorption screening dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def apply_family_corrections(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], int]:
    """Apply publication-level family corrections."""
    corrected_rows: list[dict[str, str]] = []
    correction_count = 0

    for row in rows:
        updated_row = dict(row)

        publication_id = row.get(
            "publication_id",
            "",
        ).strip()

        corrected_family = FAMILY_CORRECTIONS.get(
            publication_id
        )

        if corrected_family:
            updated_row[
                "manual_family_group"
            ] = corrected_family

            correction_count += 1

        corrected_rows.append(
            updated_row
        )

    return corrected_rows, correction_count

def write_corrected_rows(
    rows: list[dict[str, str]],
) -> Path:
    """Write the corrected consolidated screening dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No adsorption screening records were found."
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

def main() -> None:
    """Apply and write the corrected family assignments."""
    rows = read_rows()

    corrected_rows, correction_count = (
        apply_family_corrections(rows)
    )

    output_path = write_corrected_rows(
        corrected_rows
    )

    family_groups = {
        row.get(
            "manual_family_group",
            "",
        ).strip()
        for row in corrected_rows
        if row.get(
            "manual_family_group",
            "",
        ).strip()
    }

    print(
        f"Screening records processed: {len(corrected_rows)}"
    )
    print(
        f"Family assignments corrected: {correction_count}"
    )
    print(
        f"Assigned family groups after correction: "
        f"{len(family_groups)}"
    )
    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
