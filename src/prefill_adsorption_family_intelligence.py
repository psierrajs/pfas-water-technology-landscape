from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_prefilled.csv"
)

def read_intelligence_rows() -> list[dict[str, str]]:
    """Read the included-family intelligence table."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalize_text(
    value: str,
) -> str:
    """Normalize text for simple rule-based matching."""
    return (
        value.lower()
        .replace("-", " ")
        .replace("/", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
    )

def classify_treatment_mode(
    text: str,
) -> str:
    """Classify the broad treatment mode from family text."""
    if any(
        term in text
        for term in (
            "regenerat",
            "reuse",
            "reusable",
        )
    ):
        return "regeneration"

    if any(
        term in text
        for term in (
            "destroy",
            "destruction",
            "defluor",
            "degrad",
        )
    ):
        return "capture_and_destroy"

    if any(
        term in text
        for term in (
            "oxidation",
            "ozone",
            "electrochemical",
            "hydrogen peroxide",
            "treatment train",
        )
    ):
        return "combined_process"

    if any(
        term in text
        for term in (
            "adsorb",
            "activated carbon",
            "filter",
            "filtration",
        )
    ):
        return "adsorption"

    return "uncertain"


def classify_carbon_type(
    text: str,
) -> str:
    """Classify the activated-carbon form mentioned in the text."""
    if "sub micron" in text or "submicron" in text:
        return "submicron_PAC"

    if (
        "powdered activated carbon" in text
        or "powdered carbon" in text
    ):
        return "PAC"

    if (
        "granular activated carbon" in text
        or "granular carbon" in text
    ):
        return "GAC"

    if (
        "biomass activated carbon" in text
        or "biochar" in text
    ):
        return "biomass_activated_carbon"

    if any(
        term in text
        for term in (
            "modified activated carbon",
            "modified carbon",
            "swellable activated carbon",
            "colloid activated carbon",
        )
    ):
        return "modified_activated_carbon"

    if any(
        term in text
        for term in (
            "composite",
            "carbon-mno2",
            "carbon mno2",
        )
    ):
        return "carbon_composite"

    if "activated carbon" in text:
        return "unspecified_activated_carbon"

    return "uncertain"

def classify_target_matrix(
    text: str,
) -> str:
    """Classify the main water matrix or application context."""
    matches: list[str] = []

    checks = {
        "drinking_water": (
            "drinking water",
            "water purifier",
        ),
        "groundwater": (
            "groundwater",
            "ground water",
            "aquifer",
        ),
        "semiconductor_wastewater": (
            "semiconductor",
            "display panel",
        ),
        "industrial_wastewater": (
            "industrial wastewater",
            "industrial waste",
        ),
        "leachate": (
            "leachate",
            "landfill",
        ),
        "surface_water": (
            "surface water",
        ),
        "wastewater": (
            "wastewater",
            "effluent",
        ),
    }

    for label, terms in checks.items():
        if any(
            term in text
            for term in terms
        ):
            matches.append(label)

    if len(matches) > 1:
        return "multiple"

    if len(matches) == 1:
        return matches[0]

    return "unspecified"


def classify_pfas_handling(
    text: str,
) -> str:
    """Classify what ultimately happens to the captured PFAS."""
    if any(
        term in text
        for term in (
            "defluor",
            "mineraliz",
        )
    ):
        return "defluorination"

    if any(
        term in text
        for term in (
            "capture and destroy",
            "adsorption and destruction",
            "remove and destroy",
            "removing and destroying",
        )
    ):
        return "capture_and_destroy"

    if any(
        term in text
        for term in (
            "destroy",
            "destruction",
            "degrad",
        )
    ):
        return "destruction"

    if any(
        term in text
        for term in (
            "regenerat",
            "reuse",
            "reusable",
        )
    ):
        return "regeneration"

    if any(
        term in text
        for term in (
            "adsorb",
            "remove",
            "filter",
        )
    ):
        return "capture_only"

    return "uncertain"

def classify_system_configuration(
    text: str,
) -> str:
    """Classify the physical treatment configuration."""
    if any(
        term in text
        for term in (
            "in situ injection",
            "injecting activated carbon",
            "aquifer",
        )
    ):
        return "in_situ_injection"

    if any(
        term in text
        for term in (
            "mobile system",
            "shipping container",
            "containerized",
        )
    ):
        return "mobile_system"

    if any(
        term in text
        for term in (
            "treatment train",
            "combined treatment",
            "pre oxidation",
            "pre-oxidation",
        )
    ):
        return "treatment_train"

    if any(
        term in text
        for term in (
            "reactive wall",
            "permeable wall",
        )
    ):
        return "reactive_wall"

    if "column" in text:
        return "column"

    if any(
        term in text
        for term in (
            "slurry",
            "carbon slurry",
        )
    ):
        return "slurry"

    if any(
        term in text
        for term in (
            "fixed bed",
            "fixed-bed",
        )
    ):
        return "fixed_bed"

    if any(
        term in text
        for term in (
            "filter",
            "filtration",
            "water purifier",
        )
    ):
        return "filter"

    if any(
        term in text
        for term in (
            "adsorption material",
            "modified activated carbon",
            "activated carbon granules",
            "composite material",
        )
    ):
        return "material_only"

    return "uncertain"

def classify_maturity_signal(
    text: str,
) -> str:
    """Classify the strongest maturity signal visible in family text."""
    if any(
        term in text
        for term in (
            "mobile system",
            "shipping container",
            "aquifer",
            "surface water",
            "drinking water source",
        )
    ):
        return "field_deployable_system"

    if any(
        term in text
        for term in (
            "regenerat",
            "reuse",
            "reusable",
        )
    ):
        return "regeneration_process"

    if any(
        term in text
        for term in (
            "oxidation",
            "ozone",
            "electrochemical",
            "hydrogen peroxide",
            "treatment train",
        )
    ):
        return "combined_treatment_system"

    if any(
        term in text
        for term in (
            "system",
            "apparatus",
            "equipment",
            "plant",
            "device",
        )
    ):
        return "system_invention"

    if any(
        term in text
        for term in (
            "method",
            "process",
        )
    ):
        return "process_invention"

    if any(
        term in text
        for term in (
            "material",
            "granules",
            "composite",
            "activated carbon",
        )
    ):
        return "material_invention"

    return "uncertain"


def classify_strategic_theme(
    text: str,
) -> str:
    """Classify the main strategic technology theme."""
    if any(
        term in text
        for term in (
            "capture and destroy",
            "adsorption and destruction",
            "remove and destroy",
            "removing and destroying",
            "defluor",
        )
    ):
        return "capture_and_destroy"

    if any(
        term in text
        for term in (
            "regenerat",
            "reuse",
            "reusable",
        )
    ):
        return "regenerable_carbon"

    if any(
        term in text
        for term in (
            "aquifer",
            "in situ",
            "groundwater remediation",
        )
    ):
        return "in_situ_remediation"

    if any(
        term in text
        for term in (
            "semiconductor",
            "industrial wastewater",
            "industrial waste",
        )
    ):
        return "industrial_point_source"

    if any(
        term in text
        for term in (
            "mobile system",
            "shipping container",
            "containerized",
        )
    ):
        return "mobile_or_modular_treatment"

    if any(
        term in text
        for term in (
            "oxidation",
            "ozone",
            "electrochemical",
            "hydrogen peroxide",
            "treatment train",
        )
    ):
        return "combined_treatment_train"

    if any(
        term in text
        for term in (
            "modified activated carbon",
            "swellable activated carbon",
            "biomass activated carbon",
            "colloid activated carbon",
            "composite",
        )
    ):
        return "enhanced_adsorption_material"

    if any(
        term in text
        for term in (
            "activated carbon",
            "adsorption",
            "filter",
        )
    ):
        return "conventional_adsorption"

    return "uncertain"

def classify_family(
    row: dict[str, str],
) -> dict[str, str]:
    """Apply rule-based intelligence classifications to one family."""
    combined_text = " ".join(
        [
            row.get("representative_title", ""),
            row.get("assignees", ""),
            row.get("publication_ids", ""),
        ]
    )

    text = normalize_text(
        combined_text
    )

    updated_row = dict(row)

    updated_row[
        "treatment_mode"
    ] = classify_treatment_mode(text)

    updated_row[
        "carbon_type"
    ] = classify_carbon_type(text)

    updated_row[
        "target_matrix"
    ] = classify_target_matrix(text)

    updated_row[
        "pfas_handling"
    ] = classify_pfas_handling(text)

    updated_row[
        "system_configuration"
    ] = classify_system_configuration(text)

    updated_row[
        "maturity_signal"
    ] = classify_maturity_signal(text)

    updated_row[
        "strategic_theme"
    ] = classify_strategic_theme(text)

    updated_row[
        "intelligence_notes"
    ] = (
        "Initial rule-based classification from family-level "
        "title and metadata; review recommended for ambiguous cases."
    )

    return updated_row


def classify_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Classify every included patent family."""
    return [
        classify_family(row)
        for row in rows
    ]
def write_classified_rows(
    rows: list[dict[str, str]],
) -> Path:
    """Write the prefilled family intelligence dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No included patent families were found."
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
    """Print counts for the main intelligence classifications."""
    fields = (
        "treatment_mode",
        "carbon_type",
        "target_matrix",
        "pfas_handling",
        "system_configuration",
        "maturity_signal",
        "strategic_theme",
    )

    print(
        f"Patent families classified: {len(rows)}"
    )

    for field in fields:
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
    """Prefill family-level patent intelligence classifications."""
    rows = read_intelligence_rows()

    classified_rows = classify_rows(
        rows
    )

    output_path = write_classified_rows(
        classified_rows
    )

    print_summary(
        classified_rows
    )

    print(
        f"\nOutput written to: {output_path}"
    )


if __name__ == "__main__":
    main()


