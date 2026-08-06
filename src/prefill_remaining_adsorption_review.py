from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_remaining_review.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_remaining_review_prefilled.csv"
)


PREFILL_RULES = {
    "AU-2023226766-B2": {
        "decision": "include",
        "family_group": "FAM-ADS-012",
        "note": (
            "The abstract explicitly describes PFAS removal from groundwater and "
            "drinking water using sub-micron powdered activated carbon."
        ),
    },
    "CN-109019746-A": {
        "decision": "include",
        "family_group": "FAM-ADS-013",
        "note": (
            "The abstract explicitly describes activated-carbon-mediated "
            "photochemical degradation and defluorination of PFOA using indole "
            "and low-pressure mercury-lamp irradiation."
        ),
    },
    "CN-109589971-A": {
        "decision": "include",
        "family_group": "FAM-ADS-014",
        "note": (
            "The abstract describes removal of PFOA from water using a "
            "carbon-MnO2 composite with hydrogen peroxide. Activated carbon is "
            "one of the specified carbon supports, so this is retained as a "
            "carbon-based combined adsorption-and-oxidation treatment."
        ),
    },
    "CN-111171199-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-015",
        "note": (
            "The abstract describes a regenerable macroporous adsorption resin "
            "for removing perfluorinated compounds from water. It is retained as "
            "comparative adsorption context because it explicitly contrasts the "
            "resin with activated carbon rather than using activated carbon as "
            "the treatment medium."
        ),
    },
    "CN-116020413-B": {
        "decision": "include",
        "family_group": "FAM-ADS-016",
        "note": (
            "The abstract describes an activated-carbon-based adsorbent for "
            "removing perfluorinated compounds from water. Activated carbon is "
            "used as the carrier for basic yttrium chloride, producing a "
            "multifunctional adsorption material with reported high PFOA "
            "capacity."
        ),
    },
    "CN-116553707-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-017",
        "note": (
            "Electrochemical PFAS wastewater treatment; retained as related "
            "treatment context because activated carbon is not explicit in the "
            "title."
        ),
    },
    "CN-117509805-A": {
        "decision": "uncertain",
        "family_group": "",
        "note": (
            "The title confirms a column device for PFAS removal "
            "from water, but the accessible record does not establish "
            "whether activated carbon is used as the column medium."
        ),
    },
    "CN-119143232-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-018",
        "note": (
            "PFAS adsorption-coagulant for water treatment; retained as "
            "adsorption context because activated carbon is not explicit in the "
            "title."
        ),
    },
    "CN-120679486-A": {
        "decision": "include",
        "family_group": "FAM-ADS-019",
        "note": (
            "Magnetic biomass activated carbon; retained provisionally because "
            "the search match indicates PFAS/water relevance, although the title "
            "alone does not state PFAS."
        ),
    },
    "CN-121063531-A": {
        "decision": "include",
        "family_group": "FAM-ADS-020",
        "note": (
            "Modified biomass activated carbon; retained provisionally because "
            "the search match indicates PFAS/water relevance, although the title "
            "alone does not state PFAS."
        ),
    },
    "CN-121894656-A": {
        "decision": "include",
        "family_group": "FAM-ADS-021",
        "note": (
            "Colloidal activated carbon application; retained provisionally "
            "because the search match indicates PFAS/water relevance."
        ),
    },
    "EP-4665491-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-022",
        "note": (
            "Swellable activated-carbon granules; retained as an activated-carbon "
            "treatment invention identified by the PFAS-water search."
        ),
    },
    "EP-4667419-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-033",
        "note": (
            "The patent explicitly describes treatment of highly "
            "PFAS-contaminated landfill leachate and industrial "
            "liquid waste using powdered activated carbon during "
            "clariflocculation, followed by granular activated-carbon "
            "and selective-resin filtration."
        ),
    },
    "ES-2980723-T3": {
        "decision": "include",
        "family_group": "FAM-ADS-023",
        "note": (
            "Modified activated carbon and its use; retained as a core "
            "activated-carbon record identified by the PFAS-water search."
        ),
    },
    "JP-2024080892-A": {
        "decision": "include",
        "family_group": "FAM-ADS-024",
        "note": (
            "Activated carbon, water-purification filters and purifiers; retained "
            "as a core activated-carbon water-treatment record."
        ),
    },
    "JP-2026031020-A": {
        "decision": "uncertain",
        "family_group": "",
        "note": (
            "The title identifies a permeable groundwater "
            "purification wall, but the accessible record does not "
            "confirm whether activated carbon is the reactive or "
            "adsorptive medium."
        ),
    },
    "JP-7799358-B1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-025",
        "note": (
            "PFAS treatment and calcium-fluoride production; retained as broader "
            "PFAS destruction/recovery context rather than core adsorption."
        ),
    },
    "TW-202606974-A": {
        "decision": "include",
        "family_group": "FAM-ADS-034",
        "note": (
            "Taiwanese publication of a semiconductor-wastewater "
            "treatment system using acidification followed by an "
            "activated-carbon filter to adsorb PFAS. Provisionally "
            "grouped with the related TSMC publications."
        ),
    },
    "TW-I924133-B": {
        "decision": "include",
        "family_group": "FAM-ADS-034",
        "note": (
            "Taiwanese granted publication of a semiconductor-"
            "wastewater treatment system using acidification followed "
            "by an activated-carbon filter to adsorb PFAS. Provisionally "
            "grouped with the related TSMC publications."
        ),
    },
    "US-12370527-B2": {
        "decision": "include",
        "family_group": "FAM-ADS-027",
        "note": (
            "Regeneration of activated carbon; retained as a core "
            "lifecycle/regeneration record from the PFAS-water search."
        ),
    },
    "US-2022073394-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-028",
        "note": (
            "Mobile PFAS-effluent treatment system; retained provisionally as "
            "activated-carbon treatment based on the search context."
        ),
    },
    "US-2024051847-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-012",
        "note": (
            "Same Aqua-Aerobic family as AU-2023226766-B2, using sub-micron "
            "powdered activated carbon for PFAS removal."
        ),
    },
    "US-2025214875-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-029",
        "note": (
            "Explicit injection of activated carbon into a groundwater aquifer; "
            "core in-situ adsorption record."
        ),
    },
    "US-2025333344-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-030",
        "note": (
            "PFAS removal from surface water; retained provisionally as "
            "activated-carbon treatment based on the search context."
        ),
    },
    "US-2025376400-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-031",
        "note": (
            "Integrated water treatment and wet-air regeneration/destruction of "
            "PFAS; retained as capture-and-destroy context."
        ),
    },
    "US-2026021467-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-028",
        "note": (
            "Same mobile PFAS-effluent treatment family as US-2022073394-A1."
        ),
    },
    "US-2026035276-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-034",
        "note": (
            "The abstract and claims explicitly describe PFAS removal "
            "from semiconductor or display-panel wastewater using a "
            "strong-acid cation unit followed by an activated-carbon "
            "filter, preferably containing bituminous-coal carbon."
        ),
    },
    "WO-2024144448-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-035",
        "note": (
            "The patent describes chlorine-dioxide treatment of "
            "PFAS-contaminated water followed by plant-fibre filtration. "
            "Activated-carbon filters, including mixed cellulose-and-"
            "carbon filters, are explicitly included in embodiments "
            "and claims."
        ),
    },
    "WO-2024180739-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-032",
        "note": (
            "Activated carbon for water treatment; retained as a core "
            "activated-carbon record identified by the PFAS search."
        ),
    },
    "WO-2025054119-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-012",
        "note": (
            "Same Aqua-Aerobic family as AU-2023226766-B2, using sub-micron "
            "powdered activated carbon."
        ),
    },
    "WO-2026019974-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-033",
        "note": (
            "Biologically active conduit for wastewater treatment; retained only "
            "as broader treatment context."
        ),
    },
    "WO-2026080516-A1": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Bioremediation using an aerobic bacterium; outside activated-carbon "
            "adsorption."
        ),
    },
    "AU-2017371390-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-034",
        "note": (
            "Treatment of persistent organic pollutants; retained as broad "
            "remediation context, with activated-carbon relevance not confirmed "
            "by the title."
        ),
    },
    "CN-104773884-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-035",
        "note": (
            "Iron-carbon micro-electrolysis and photodegradation of PFOA; "
            "relevant combined treatment but not clearly activated carbon."
        ),
    },
    "CN-106880095-A": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Water-repellent work clothing; irrelevant to PFAS water treatment."
        ),
    },
    "CN-113354587-A": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Drying of a fluorine-containing lithium salt; irrelevant to PFAS "
            "water treatment."
        ),
    },
    "CN-118032890-A": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Electrochemical sensor for perfluorooctane; analytical detection "
            "rather than water treatment."
        ),
    },
    "CN-120586853-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-036",
        "note": (
            "The invention uses silane-modified magnetite "
            "nanoparticles to adsorb PFOS from water. It is retained "
            "as comparative adsorption context because the material "
            "is presented as outperforming conventional activated "
            "carbon rather than using activated carbon."
        ),
    },
    "CN-121198221-A": {
        "decision": "uncertain",
        "family_group": "",
        "note": (
            "The title identifies an adsorbent and its application, "
            "but the accessible information does not establish its "
            "composition or confirm activated-carbon use in PFAS "
            "water treatment."
        ),
    },
    "CN-121698443-A": {
        "decision": "context_only",
        "family_group": "FAM-ADS-036",
        "note": (
            "Fenton treatment system; retained as destructive-treatment context, "
            "not activated-carbon adsorption."
        ),
    },
    "CN-200987841-Y": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Protective clothing; irrelevant to PFAS water treatment."
        ),
    },
    "GB-953152-A": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Fluorine-containing elastomeric copolymers; irrelevant to PFAS water "
            "treatment."
        ),
    },
    "GR-1006855-B": {
        "decision": "exclude",
        "family_group": "FAM-ADS-037",
        "note": (
            "Construction materials from solid wastes; irrelevant to PFAS water "
            "treatment."
        ),
    },
    "GR-20060100233-A": {
        "decision": "exclude",
        "family_group": "FAM-ADS-037",
        "note": (
            "Same Greek construction-material family; irrelevant to PFAS water "
            "treatment."
        ),
    },
    "JP-2026057649-A": {
        "decision": "include",
        "family_group": "FAM-ADS-037",
        "note": (
            "The patent explicitly processes activated carbon that "
            "has adsorbed PFAS. PFAS is extracted from the carbon "
            "using methanol and destroyed by alkaline ozone treatment, "
            "while the treated activated carbon can be reused."
        ),
    },
    "JP-H03151304-A": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Freshness-keeping agent; irrelevant to PFAS water treatment."
        ),
    },
    "US-12037266-B2": {
        "decision": "include",
        "family_group": "FAM-ADS-038",
        "note": (
            "Reusable composite filter for removing and destroying molecular "
            "contaminants from water; retained provisionally as a "
            "PFAS/activated-carbon filter record."
        ),
    },
    "US-2010000947-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-039",
        "note": (
            "Treatment of fluorinated-surfactant aqueous solution; retained as "
            "historical PFAS-treatment context."
        ),
    },
    "US-2024300831-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-038",
        "note": (
            "Same Corewater reusable composite-filter family as US-12037266-B2."
        ),
    },
    "US-8039665-B2": {
        "decision": "exclude",
        "family_group": "",
        "note": (
            "Production of fluorine-containing carboxylic acid ester; irrelevant "
            "to PFAS water treatment."
        ),
    },
    "WO-2025210445-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-040",
        "note": (
            "Electrochemical removal of pollutants from water; retained as "
            "related treatment context, not core activated-carbon adsorption."
        ),
    },
    "WO-2025240732-A1": {
        "decision": "include",
        "family_group": "FAM-ADS-038",
        "note": (
            "Same Corewater reusable composite-filter family as the corresponding "
            "US records."
        ),
    },
    "WO-2026037982-A1": {
        "decision": "context_only",
        "family_group": "FAM-ADS-041",
        "note": (
            "Silicate adsorbent for water treatment; relevant comparative "
            "adsorption context but not activated carbon."
        ),
    },
}


def read_review_rows() -> list[dict[str, str]]:
    """Read the remaining adsorption review dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def apply_prefill_rules(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Apply provisional decisions to matching records."""
    output_rows: list[dict[str, str]] = []

    for row in rows:
        updated_row = dict(row)

        publication_id = row.get(
            "publication_id",
            "",
        ).strip()

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
    """Write the updated remaining-review dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No remaining adsorption records were found."
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
    """Print counts for the current prefilled review."""
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
        f"Remaining review records: {len(rows)}"
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
    """Apply prefills to the remaining adsorption review."""
    rows = read_review_rows()

    prefilled_rows = apply_prefill_rules(
        rows
    )

    output_path = write_prefilled_csv(
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
