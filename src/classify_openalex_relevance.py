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
    r"\blandfill\b",
    r"\bAFFF\b",
    r"\baqueous film[- ]forming foam\b",
    r"\bcontaminated material",
    r"\bspent media\b",
    r"\bspent adsorbent",
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

    if title_has_pfas and title_has_water and title_has_treatment:
        return "water_treatment", signals

    if (
        title_has_pfas
        and title_has_adjacent_matrix
        and title_has_treatment
    ):
        return "adjacent_matrix", signals

    if has_pfas and has_water and has_treatment:
        return "water_treatment", signals

    if has_pfas and has_adjacent_matrix and has_treatment:
        return "adjacent_matrix", signals

    if has_pfas and has_treatment:
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
