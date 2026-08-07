from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_summary.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence.csv"
)


TREATMENT_MODES = {
    "adsorption",
    "regeneration",
    "capture_and_destroy",
    "combined_process",
    "uncertain",
}

CARBON_TYPES = {
    "GAC",
    "PAC",
    "submicron_PAC",
    "modified_activated_carbon",
    "biomass_activated_carbon",
    "carbon_composite",
    "unspecified_activated_carbon",
    "other",
    "uncertain",
}

TARGET_MATRICES = {
    "drinking_water",
    "groundwater",
    "wastewater",
    "industrial_wastewater",
    "semiconductor_wastewater",
    "leachate",
    "surface_water",
    "multiple",
    "unspecified",
}

PFAS_HANDLING_MODES = {
    "capture_only",
    "regeneration",
    "destruction",
    "defluorination",
    "capture_and_destroy",
    "uncertain",
}

SYSTEM_CONFIGURATIONS = {
    "fixed_bed",
    "slurry",
    "column",
    "in_situ_injection",
    "mobile_system",
    "treatment_train",
    "filter",
    "reactive_wall",
    "material_only",
    "other",
    "uncertain",
}

MATURITY_SIGNALS = {
    "material_invention",
    "process_invention",
    "system_invention",
    "field_deployable_system",
    "regeneration_process",
    "combined_treatment_system",
    "uncertain",
}

STRATEGIC_THEMES = {
    "conventional_adsorption",
    "enhanced_adsorption_material",
    "regenerable_carbon",
    "capture_and_destroy",
    "in_situ_remediation",
    "industrial_point_source",
    "mobile_or_modular_treatment",
    "combined_treatment_train",
    "other",
    "uncertain",
}


def read_family_rows() -> list[dict[str, str]]:
    """Read the adsorption patent-family summary."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def is_included_family(
    row: dict[str, str],
) -> bool:
    """Return True when the family has an include decision."""
    decisions = {
        decision.strip()
        for decision in row.get(
            "decisions",
            "",
        ).split(";")
        if decision.strip()
    }

    return "include" in decisions

def empty_intelligence_fields() -> dict[str, str]:
    """Return blank intelligence fields for one patent family."""
    return {
        "treatment_mode": "",
        "carbon_type": "",
        "target_matrix": "",
        "pfas_handling": "",
        "system_configuration": "",
        "maturity_signal": "",
        "strategic_theme": "",
        "intelligence_notes": "",
    }


def build_intelligence_rows(
    family_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Create an intelligence-review table for included families."""
    output_rows: list[dict[str, str]] = []

    for row in family_rows:
        if not is_included_family(row):
            continue

        output_row = dict(row)
        output_row.update(
            empty_intelligence_fields()
        )

        output_rows.append(
            output_row
        )

    return output_rows

def write_intelligence_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the included-family intelligence review table."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No included adsorption patent families were found."
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
    """Create the family-level patent intelligence review table."""
    family_rows = read_family_rows()

    intelligence_rows = build_intelligence_rows(
        family_rows
    )

    output_path = write_intelligence_csv(
        intelligence_rows
    )

    print(
        f"Included patent families: {len(intelligence_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()


