from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_uncertain_review.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_high_priority_prefilled.csv"
)

HIGH_PRIORITY_THRESHOLD = 2

def read_review_rows() -> list[dict[str, str]]:
    """Read the prioritized adsorption review dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def is_high_priority(
    row: dict[str, str],
) -> bool:
    """Return True for records meeting the priority threshold."""
    value = row.get(
        "review_priority",
        "0",
    ).strip()

    return int(value or 0) >= HIGH_PRIORITY_THRESHOLD

PREFILL_RULES = {
        "CN-121872623-A": {
        "decision": "include",
        "family_group": "FAM-ADS-010",
        "note": (
            "The abstract explicitly describes emergency PFOA "
            "removal from drinking-water source water using "
            "ultrafine powdered activated carbon adsorption, "
            "combined with ozone and hydrogen peroxide "
            "pre-oxidation."
        ),
    },
    "JP-2024139775-A": {
        "decision": "include",
        "family_group": "FAM-ADS-001",
        "note": (
            "Title explicitly describes adsorption treatment "
            "using powdered activated carbon."
        ),
    },
    "US-2020206793-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-002",
        "note": (
            "Relevant PFAS removal and concentration process, "
            "but activated carbon is not explicit in the title."
        ),
    },
    "US-2020262719-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-003",
        "note": (
            "Relevant in-situ PFAS groundwater remediation "
            "using sorptive media, but the title does not "
            "explicitly identify activated carbon."
        ),
    },
    "CN-121269996-A": {
        "decision": "include",
        "family_group": "FAM-ADS-011",
        "note": (
            "The abstract explicitly describes PFAS wastewater "
            "treatment using activated-carbon-based packing layers "
            "combined with electrode plates, heating, calcium "
            "carbonate and calcium hydroxide."
        ),
    },
    "JP-7817717-B1": {
        "decision": "include",
        "family_group": "FAM-ADS-004",
        "note": (
            "Title explicitly concerns activated carbon, "
            "adsorption filters and water purification."
        ),
    },
    "WO-2025106791-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-005",
        "note": (
            "Relevant combined PFAS adsorption-and-destruction "
            "system; retain as capture-and-destroy context."
        ),
    },
    "JP-2024030815-A": {
        "decision": "include",
        "family_group": "FAM-ADS-009",
        "note": (
            "The abstract and claims explicitly describe "
            "PFOS/PFOA removal from liquid using activated "
            "carbon combined with ozone treatment."
        ),
    },
    "AU-2023277470-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-006",
        "note": (
            "Relevant PFAS removal using modified granular "
            "media, but activated carbon is not explicit."
        ),
    },
    "CA-3245600-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-007",
        "note": (
            "Relevant combined PFAS treatment using bioreactors "
            "and supercritical water oxidation, but it is not "
            "an activated-carbon invention."
        ),
    },
    "AU-2021206880-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-008",
        "note": (
            "Relevant filtration-media invention for PFAS "
            "removal, but activated carbon is not explicit."
        ),
    },
    "US-2022041467-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-008",
        "note": (
            "Same Environmental Water Solutions filtration-media "
            "invention in another jurisdiction."
        ),
    },
    "US-2020108429-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-002",
        "note": (
            "Likely related to the Brady porous-media PFAS "
            "removal family; activated carbon is not explicit."
        ),
    },
    "US-2013316433-A1": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Enzymatic transformation of PFAS in soil or "
            "groundwater; outside activated-carbon adsorption."
        ),
    },
}

def apply_prefill_rules(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Apply provisional decisions to high-priority records."""
    output_rows: list[dict[str, str]] = []

    for row in rows:
        if not is_high_priority(row):
            continue

        publication_id = row.get(
            "publication_id",
            "",
        ).strip()

        updated_row = dict(row)

        rule = PREFILL_RULES.get(
            publication_id
        )

        if rule:
            updated_row[
                "manual_relevance_decision"
            ] = rule["decision"]

            updated_row[
                "manual_family_group"
            ] = rule["family_group"]

            updated_row[
                "manual_screening_notes"
            ] = rule["note"]

        output_rows.append(
            updated_row
        )

    return output_rows

def write_prefilled_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the prefilled high-priority review file."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No high-priority records were available."
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

def print_prefill_summary(
    rows: list[dict[str, str]],
) -> None:
    """Print counts for the provisional decisions."""
    counts: dict[str, int] = {}

    for row in rows:
        decision = row.get(
            "manual_relevance_decision",
            "",
        ).strip() or "blank"

        counts[decision] = counts.get(
            decision,
            0,
        ) + 1

    print(
        f"High-priority records prefilled: {len(rows)}"
    )

    for decision in (
        "include",
        "context_only",
        "uncertain",
        "exclude",
        "blank",
    ):
        if decision in counts:
            print(
                f"{decision}: {counts[decision]}"
            )


def main() -> None:
    """Prefill the high-priority adsorption review."""
    rows = read_review_rows()

    prefilled_rows = apply_prefill_rules(
        rows
    )

    output_path = write_prefilled_csv(
        prefilled_rows
    )

    print_prefill_summary(
        prefilled_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
