from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_review.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_review_prefilled.csv"
)

def read_review_rows() -> list[dict[str, str]]:
    """Read the family intelligence review dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalize_text(
    value: str,
) -> str:
    """Normalize text for targeted rule matching."""
    return (
        value.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
    )

TARGETED_PREFILL_RULES = {
    "FAM-ADS-001": {
        "treatment_mode": "adsorption",
        "carbon_type": "PAC",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "slurry",
        "maturity_signal": "process_invention",
        "strategic_theme": "conventional_adsorption",
        "intelligence_notes": (
            "Powdered activated-carbon adsorption treatment "
            "for organic fluorine compounds."
        ),
    },
    "FAM-ADS-009": {
        "treatment_mode": "combined_process",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_and_destroy",
        "system_configuration": "treatment_train",
        "maturity_signal": "combined_treatment_system",
        "strategic_theme": "combined_treatment_train",
        "intelligence_notes": (
            "Activated-carbon adsorption is combined with ozone "
            "treatment for PFOS/PFOA removal."
        ),
    },
    "FAM-ADS-010": {
        "treatment_mode": "combined_process",
        "carbon_type": "PAC",
        "target_matrix": "drinking_water",
        "pfas_handling": "capture_only",
        "system_configuration": "treatment_train",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "combined_treatment_train",
        "intelligence_notes": (
            "Emergency drinking-water treatment combines ozone/"
            "hydrogen-peroxide pre-oxidation with ultrafine "
            "powdered activated-carbon adsorption."
        ),
    },

    "FAM-ADS-011": {
        "treatment_mode": "combined_process",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "wastewater",
        "pfas_handling": "destruction",
        "system_configuration": "other",
        "maturity_signal": "combined_treatment_system",
        "strategic_theme": "combined_treatment_train",
        "intelligence_notes": (
            "PFAS wastewater treatment uses activated-carbon-based "
            "packing together with electrode plates, heating and "
            "alkaline mineral additives, with degradation claimed."
        ),
    },
    "FAM-ADS-012": {
        "treatment_mode": "adsorption",
        "carbon_type": "submicron_PAC",
        "target_matrix": "multiple",
        "pfas_handling": "capture_only",
        "system_configuration": "slurry",
        "maturity_signal": "process_invention",
        "strategic_theme": "conventional_adsorption",
        "intelligence_notes": (
            "PFAS and other recalcitrant organics are removed from "
            "groundwater and drinking water using sub-micron "
            "powdered activated carbon."
        ),
    },
    "FAM-ADS-013": {
        "treatment_mode": "capture_and_destroy",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "defluorination",
        "system_configuration": "other",
        "maturity_signal": "process_invention",
        "strategic_theme": "capture_and_destroy",
        "intelligence_notes": (
            "Activated carbon participates in photochemical PFOA "
            "degradation and defluorination using indole and "
            "low-pressure mercury-lamp irradiation."
        ),
    },

    "FAM-ADS-014": {
        "treatment_mode": "combined_process",
        "carbon_type": "carbon_composite",
        "target_matrix": "unspecified",
        "pfas_handling": "destruction",
        "system_configuration": "material_only",
        "maturity_signal": "combined_treatment_system",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "A carbon-MnO2 composite, with activated carbon among "
            "the possible carbon supports, is combined with hydrogen "
            "peroxide for PFOA removal from water."
        ),
    },
    "FAM-ADS-016": {
        "treatment_mode": "adsorption",
        "carbon_type": "modified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Basic yttrium chloride supported on activated carbon "
            "provides a multifunctional adsorbent for removal of "
            "perfluorinated compounds from water."
        ),
    },
    "FAM-ADS-019": {
        "treatment_mode": "adsorption",
        "carbon_type": "biomass_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Magnetic biomass-derived activated carbon is developed "
            "as an enhanced adsorption material for PFAS treatment."
        ),
    },

    "FAM-ADS-020": {
        "treatment_mode": "adsorption",
        "carbon_type": "biomass_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Alkali-acid synergistically modified biomass activated "
            "carbon is developed as an enhanced PFAS adsorption material."
        ),
    },
    "FAM-ADS-021": {
        "treatment_mode": "adsorption",
        "carbon_type": "modified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Colloidal activated carbon is developed as a modified "
            "carbon material for PFAS adsorption applications."
        ),
    },
    "FAM-ADS-022": {
        "treatment_mode": "adsorption",
        "carbon_type": "modified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Swellable activated-carbon granules represent an engineered "
            "adsorbent material aimed at improving contaminant capture."
        ),
    },

    "FAM-ADS-023": {
        "treatment_mode": "adsorption",
        "carbon_type": "modified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "material_only",
        "maturity_signal": "material_invention",
        "strategic_theme": "enhanced_adsorption_material",
        "intelligence_notes": (
            "Modified activated carbon is developed as an improved "
            "adsorbent material for contaminant removal applications."
        ),
    },
    "FAM-ADS-024": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "drinking_water",
        "pfas_handling": "capture_only",
        "system_configuration": "filter",
        "maturity_signal": "system_invention",
        "strategic_theme": "conventional_adsorption",
        "intelligence_notes": (
            "Activated carbon is incorporated into water-purification "
            "filters and purifier systems for contaminant removal."
        ),
    },
    "FAM-ADS-027": {
        "treatment_mode": "regeneration",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "regeneration",
        "system_configuration": "other",
        "maturity_signal": "regeneration_process",
        "strategic_theme": "regenerable_carbon",
        "intelligence_notes": (
            "The invention focuses on regeneration of spent activated "
            "carbon, extending adsorbent life and reducing disposal needs."
        ),
    },

    "FAM-ADS-028": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "wastewater",
        "pfas_handling": "capture_only",
        "system_configuration": "mobile_system",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "mobile_or_modular_treatment",
        "intelligence_notes": (
            "A mobile PFAS effluent-treatment system configured in a "
            "shipping container indicates a deployable, modular treatment "
            "approach using activated-carbon-based capture."
        ),
    },
    "FAM-ADS-029": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "groundwater",
        "pfas_handling": "capture_only",
        "system_configuration": "in_situ_injection",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "in_situ_remediation",
        "intelligence_notes": (
            "Activated carbon is injected directly into a groundwater "
            "aquifer, representing an in-situ remediation strategy."
        ),
    },
    "FAM-ADS-030": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "surface_water",
        "pfas_handling": "capture_only",
        "system_configuration": "treatment_train",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "combined_treatment_train",
        "intelligence_notes": (
            "The invention targets PFAS removal from surface water using "
            "a system-level treatment configuration rather than a material "
            "invention alone."
        ),
    },

    "FAM-ADS-032": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_only",
        "system_configuration": "filter",
        "maturity_signal": "material_invention",
        "strategic_theme": "conventional_adsorption",
        "intelligence_notes": (
            "Activated carbon is developed specifically for water "
            "treatment, representing a conventional adsorption-focused "
            "material application."
        ),
    },
    "FAM-ADS-033": {
        "treatment_mode": "combined_process",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "leachate",
        "pfas_handling": "capture_only",
        "system_configuration": "treatment_train",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "combined_treatment_train",
        "intelligence_notes": (
            "Treatment of highly PFAS-contaminated liquids combines "
            "powdered activated carbon during clarification with "
            "granular activated-carbon and selective-resin filtration."
        ),
    },
    "FAM-ADS-034": {
        "treatment_mode": "adsorption",
        "carbon_type": "GAC",
        "target_matrix": "semiconductor_wastewater",
        "pfas_handling": "capture_only",
        "system_configuration": "filter",
        "maturity_signal": "field_deployable_system",
        "strategic_theme": "industrial_point_source",
        "intelligence_notes": (
            "Semiconductor-process wastewater is treated using "
            "acidification or ion treatment followed by a "
            "bituminous-coal activated-carbon filter for PFAS capture."
        ),
    },

    "FAM-ADS-035": {
        "treatment_mode": "combined_process",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_and_destroy",
        "system_configuration": "treatment_train",
        "maturity_signal": "combined_treatment_system",
        "strategic_theme": "capture_and_destroy",
        "intelligence_notes": (
            "PFAS decontamination combines chemical treatment "
            "with downstream filtration, including activated-carbon "
            "filter configurations, linking capture with destruction."
        ),
    },
    "FAM-ADS-037": {
        "treatment_mode": "regeneration",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_and_destroy",
        "system_configuration": "other",
        "maturity_signal": "regeneration_process",
        "strategic_theme": "capture_and_destroy",
        "intelligence_notes": (
            "PFAS-loaded activated carbon is treated to extract PFAS "
            "for subsequent alkaline ozone destruction, while the "
            "activated carbon can be reused."
        ),
    },
    "FAM-ADS-038": {
        "treatment_mode": "capture_and_destroy",
        "carbon_type": "carbon_composite",
        "target_matrix": "unspecified",
        "pfas_handling": "capture_and_destroy",
        "system_configuration": "filter",
        "maturity_signal": "combined_treatment_system",
        "strategic_theme": "capture_and_destroy",
        "intelligence_notes": (
            "A reusable composite filter material is designed both "
            "to remove and destroy molecular contaminants from water, "
            "representing an integrated capture-and-destroy approach."
        ),
    },

    "FAM-ADS-004": {
        "treatment_mode": "adsorption",
        "carbon_type": "unspecified_activated_carbon",
        "target_matrix": "drinking_water",
        "pfas_handling": "capture_only",
        "system_configuration": "filter",
        "maturity_signal": "system_invention",
        "strategic_theme": "conventional_adsorption",
        "intelligence_notes": (
            "Activated carbon is incorporated into adsorption filters "
            "and water-purifier configurations, representing a "
            "conventional activated-carbon capture approach."
        ),
    },
}

def apply_targeted_rules(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Apply family-specific intelligence classifications."""
    output_rows: list[dict[str, str]] = []

    for row in rows:
        updated_row = dict(row)

        family_group = row.get(
            "family_group",
            "",
        ).strip()

        rule = TARGETED_PREFILL_RULES.get(
            family_group
        )

        if rule:
            for field, value in rule.items():
                updated_row[field] = value

        output_rows.append(
            updated_row
        )

    return output_rows

def write_prefilled_rows(
    rows: list[dict[str, str]],
) -> Path:
    """Write the targeted family intelligence review dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No family intelligence review records were found."
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
    """Print remaining uncertain classifications."""
    intelligence_fields = (
        "treatment_mode",
        "carbon_type",
        "target_matrix",
        "pfas_handling",
        "system_configuration",
        "maturity_signal",
        "strategic_theme",
    )

    print(
        f"Review families processed: {len(rows)}"
    )

    for field in intelligence_fields:
        uncertain_count = sum(
            1
            for row in rows
            if row.get(
                field,
                "",
            ).strip() == "uncertain"
        )

        print(
            f"{field} uncertain: {uncertain_count}"
        )

def main() -> None:
    """Apply targeted intelligence classifications."""
    rows = read_review_rows()

    prefilled_rows = apply_targeted_rules(
        rows
    )

    output_path = write_prefilled_rows(
        prefilled_rows
    )

    print_summary(
        prefilled_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()

