from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


PFAS_PATTERNS = [
    r"\bPFAS(?:s)?\b",
    r"\bPFAA(?:s)?\b",
    r"\bPFOA\b",
    r"\bPFOS\b",
    r"\bperfluorooctanoic acid\b",
    r"\bperfluorooctane sulfonic acid\b",
    r"\bperfluorooctanesulfonic acid\b",
    r"\bperfluorooctane sulfonate\b",
    r"\bperfluorooctanesulfonate\b",
    r"\bPFBS\b",
    r"\bPFHxS\b",
    r"\bPFNA\b",
    r"\bGenX\b",
    r"\bHFPO[- ]DA\b",
    r"\bper[- ]?\s*and\s+poly[- ]?fluoroalkyl\b",
    r"\bper[- ]?fluoroalkyl\b",
    r"\bpoly[- ]?fluoroalkyl\b",
    r"\bperfluorinated\b",
    r"\bpolyfluorinated\b",
    r"\bfluorotelomer",
    r"\baqueous film[- ]forming foam\b",
    r"\bAFFF\b",
]

WATER_PATTERNS = [
    r"\bwater\b",
    r"\bwastewaters?\b",
    r"\bgroundwaters?\b",
    r"\bdrinking waters?\b",
    r"\bsurface water\b",
    r"\baqueous\b",
    r"\bleachate\b",
    r"\beffluent\b",
    r"\binfluent\b",
    r"\bwater treatment\b",
    r"\bwater reuse\b",
    r"\bmembrane concentrate",
    r"\breverse osmosis\b",
    r"\bnanofiltration\b",
    r"\bRO membrane",
    r"\baqueous matrices\b",
    r"\bwater system",
    r"\bmembrane(?:s)?\b",
    r"\bfiltration\b",
]

ADJACENT_MATRIX_PATTERNS = [
    r"\bsoil\b",
    r"\bsediment\b",
    r"\bsludge\b",
    r"\bbiosolid",
    r"\bsolid waste\b",
    r"\bcontaminated material",
    r"\bspent media\b",
    r"\bspent adsorbent",
    r"\bspent sorbent",
    r"\bspent engineered sorbent",
    r"\btreatment residual",
    r"\bwater treatment residual",
]

# These patterns indicate that a solid or residual material is
# itself the treatment target. Generic mentions of residuals are
# not enough because residual materials may instead be sorbents
# used to remove PFAS from water.
TITLE_ADJACENT_TARGET_PATTERNS = [
    # Explicit treatment of solid or residual matrices.
    r"\b(?:treat\w*|remediat\w*|degrad\w*|destroy\w*|"
    r"destruction|stabili[sz]\w*|pyrolysis|"
    r"hydrothermal liquefaction)\b"
    r"[^\n]{0,120}\b(?:soil|sediment|sludge|biosolids?|"
    r"solid wastes?|spent media|spent sorbents?)\b",

    # Matrix first, followed by an explicit treatment action.
    r"\b(?:soil|sediment|sludge|biosolids?|solid wastes?|"
    r"spent media|spent sorbents?)\b"
    r"[^\n]{0,120}\b(?:treat\w*|remediat\w*|degrad\w*|"
    r"destroy\w*|destruction|stabili[sz]\w*|pyrolysis|"
    r"hydrothermal liquefaction)\b",

    # Reviews specifically centred on solid matrices.
    r"\b(?:occurrence|fate|remediation|management)\b"
    r"[^\n]{0,100}\b(?:in|of)\b"
    r"[^\n]{0,80}\b(?:soil|sludge|biosolids?)\b",

    r"\bdestruction\s+of\s+spent\s+(?:media|sorbents?)\b",
    r"\bfate\s+of\b[^\n]{0,100}\bduring\b"
    r"[^\n]{0,100}\bsludge\b",
]


# Mixed-matrix titles that explicitly include water remain relevant
# to the core water-treatment landscape.
TITLE_MIXED_WATER_TREATMENT_PATTERNS = [
    r"\b(?:degradation|removal|treatment|remediation)\b"
    r"[^\n]{0,100}\bwater and soil\b",
    r"\bwater and soil\b[^\n]{0,100}"
    r"\b(?:degradation|removal|treatment|remediation)\b",
]

# Titles about measurement, occurrence or management of residuals
# are contextual rather than treatment studies.
TITLE_RESIDUAL_CONTEXT_PATTERNS = [
    r"\bcharacteriz\w*\b[^\n]{0,100}"
    r"\btreatment residuals?\b",
    r"\bconcentrations?\b[^\n]{0,100}"
    r"\btreatment residuals?\b",
    r"\bmanagement pathways?\b[^\n]{0,100}"
    r"\bspent media\b",
    r"\bspent media management\b",
]


TREATMENT_PATTERNS = [
    r"\btreat",
    r"\bremov",
    r"\bremediat",
    r"\bdegrad",
    r"\bdestroy",
    r"\bdestruction\b",
    r"\bmineraliz",
    r"\bdefluorinat",
    r"\bseparat",
    r"\badsorp",
    r"\bsorption\b",
    r"\bion exchange\b",
    r"\bmembrane\b",
    r"\bfiltration\b",
    r"\boxidation\b",
    r"\bplasma\b",
    r"\bsonolysis\b",
    r"\bphotocatal",
    r"\bpyrolysis\b",
    r"\bincineration\b",
    r"\bhydrothermal\b",
    r"\bsupercritical water oxidation\b",
    r"\bbiodegradation\b",
    r"\bbioremediation\b",
    r"\brejection\b",
    r"\bretention\b",
    r"\bremoval\b",
    r"\breverse osmosis\b",
    r"\bnanofiltration\b",
    r"\bRO membrane",
    r"\badsorbent",
    r"\bsorbent",
]

CONTEXT_PATTERNS = [
    r"\boccurrence\b",
    r"\bfate\b",
    r"\btransport\b",
    r"\btoxicity\b",
    r"\btoxicolog",
    r"\bexposure\b",
    r"\bmonitoring\b",
    r"\banalytical method",
    r"\bregulation\b",
    r"\bpolicy\b",
    r"\brisk assessment\b",
    r"\bbioaccumul",
    r"\becotoxic",
    r"\bmanagement strateg",
    r"\bdisposal\b",
    r"\bwaste management\b",
    r"\blife[- ]cycle\b",
    r"\benvironmental distribution\b",
    r"\bsources?\b",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read classified OpenAlex records."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def matches_any(text: str, patterns: list[str]) -> bool:
    """Return True when any pattern matches the supplied text."""
    return any(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for pattern in patterns
    )


def classify_relevance(
    title: str,
    abstract: str,
) -> tuple[str, list[str]]:
    """Assign a conservative scope-relevance label."""
    title_text = title.strip()
    full_text = f"{title}\n{abstract}".strip()

    title_has_pfas = matches_any(title_text, PFAS_PATTERNS)
    title_has_water = matches_any(title_text, WATER_PATTERNS)
    title_has_adjacent_matrix = matches_any(
        title_text,
        ADJACENT_MATRIX_PATTERNS,
    )
    title_has_adjacent_target = matches_any(
        title_text,
        TITLE_ADJACENT_TARGET_PATTERNS,
    )
    title_has_mixed_water_treatment = matches_any(
        title_text,
        TITLE_MIXED_WATER_TREATMENT_PATTERNS,
    )
    title_has_residual_context = matches_any(
        title_text,
        TITLE_RESIDUAL_CONTEXT_PATTERNS,
    )
    title_has_treatment = matches_any(
        title_text,
        TREATMENT_PATTERNS,
    )

    has_pfas = matches_any(full_text, PFAS_PATTERNS)
    has_water = matches_any(full_text, WATER_PATTERNS)
    has_adjacent_matrix = matches_any(
        full_text,
        ADJACENT_MATRIX_PATTERNS,
    )
    has_treatment = matches_any(full_text, TREATMENT_PATTERNS)
    has_context = matches_any(full_text, CONTEXT_PATTERNS)

    signals = []

    if has_pfas:
        signals.append("pfas")

    if has_water:
        signals.append("water")

    if has_adjacent_matrix:
        signals.append("adjacent_matrix")

    if has_treatment:
        signals.append("treatment")

    if has_context:
        signals.append("context")

    # Measurement or management of treatment residuals is
    # contextual rather than direct PFAS treatment.
    if title_has_pfas and title_has_residual_context:
        return "contextual", signals

    # Explicit mixed water-and-soil treatment remains part of the
    # core water-treatment landscape.
    if (
        title_has_pfas
        and title_has_mixed_water_treatment
        and title_has_treatment
    ):
        return "water_treatment", signals

    # Explicit solid or residual matrices in the title take
    # precedence over incidental water-related terminology.
    if (
        title_has_pfas
        and title_has_adjacent_target
        and title_has_treatment
    ):
        return "adjacent_matrix", signals

    if title_has_pfas and title_has_water and title_has_treatment:
        return "water_treatment", signals

    # At full-text level, water treatment takes precedence.
    # Abstracts often mention soil, sludge or spent media only as
    # background, comparison matrices or downstream residuals.
    if has_pfas and has_water and has_treatment:
        return "water_treatment", signals

    if has_pfas and has_adjacent_matrix and has_treatment:
        return "adjacent_matrix", signals

    # Use the unspecified-matrix category only when the title itself
    # provides evidence of both PFAS and treatment. This avoids
    # promoting contextual papers because their abstracts contain
    # generic words such as "degradation" or "removal".
    if title_has_pfas and title_has_treatment:
        return "treatment_unspecified_matrix", signals

    if has_pfas and (
        has_context
        or has_water
        or has_adjacent_matrix
    ):
        return "contextual", signals

    return "likely_irrelevant", signals

def classify_records(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Add relevance fields to every classified record."""
    enriched_rows = []

    for row in rows:
        relevance_label, relevance_signals = classify_relevance(
            row.get("title", ""),
            row.get("abstract", ""),
        )

        enriched = dict(row)
        enriched["relevance_label"] = relevance_label
        enriched["relevance_signals"] = ";".join(relevance_signals)
        enriched["relevance_method"] = "title_abstract_rules"
        enriched_rows.append(enriched)

    return enriched_rows


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    """Write relevance-classified records."""
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        raise ValueError("No records available to write")

    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Assign initial PFAS water-landscape relevance labels."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/processed/openalex_classified.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/processed/openalex_relevance_classified.csv"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    classified = classify_records(rows)
    write_csv(classified, args.output)

    counts: dict[str, int] = {}

    for row in classified:
        label = str(row["relevance_label"])
        counts[label] = counts.get(label, 0) + 1

    print(f"Input records: {len(rows)}")

    for label in (
        "water_treatment",
        "adjacent_matrix",
        "treatment_unspecified_matrix",
        "contextual",
        "likely_irrelevant",
    ):
        print(f"{label}: {counts.get(label, 0)}")

    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
