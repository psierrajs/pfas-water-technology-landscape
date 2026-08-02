from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any


TECHNOLOGY_RULES = {
    "adsorption": [
        r"\badsorp",
        r"\bactivated carbon\b",
        r"\bbiochar\b",
        r"\bgranular activated carbon\b",
        r"\bgac\b",
        r"\bporous material",
    ],
    "ion_exchange": [
        r"\bion exchange\b",
        r"\banion exchange\b",
        r"\bexchange resin",
        r"\bresin regeneration\b",
    ],
    "membranes": [
        r"\breverse osmosis\b",
        r"\bnanofiltration\b",
        r"\bmembrane filtration\b",
        r"\bmembrane separation\b",
        r"\bfunctionalized membrane",
    ],
    "electrochemical_oxidation": [
        r"\belectrochemical oxidation\b",
        r"\belectrooxidation\b",
        r"\belectro-oxidation\b",
        r"\belectrochemical degradation\b",
        r"\banodic oxidation\b",
        r"\bboron-doped diamond\b",
    ],
    "plasma": [
        r"\bplasma\b",
        r"\bnon-thermal plasma\b",
        r"\bnonthermal plasma\b",
        r"\bcold atmospheric plasma\b",
        r"\bplasma-based\b",
    ],
    "photocatalysis": [
        r"\bphotocatal",
        r"\bphotochemical degradation\b",
        r"\buv[- ]assisted\b",
        r"\blight-driven degradation\b",
    ],
    "sonolysis": [
        r"\bsonolysis\b",
        r"\bsonochemical\b",
        r"\bultrasonic degradation\b",
        r"\bultrasound treatment\b",
        r"\bsonoluminescence\b",
    ],
    "supercritical_water_oxidation": [
        r"\bsupercritical water oxidation\b",
        r"\bscwo\b",
    ],
    "hydrothermal": [
        r"\bhydrothermal liquefaction\b",
        r"\balkaline hydrothermal\b",
        r"\bhydrothermal "
        r"(?:treatment|processing|process|degradation|destruction)\b",
        r"\bhydrothermal(?:ly)? (?:degrad|destroy|treat)",
    ],
    "thermal": [
        r"\bthermal destruction\b",
        r"\bthermal degradation\b",
        r"\bPFAS.{0,120}\bthermal treatment\b",
        r"\bthermal treatment\b.{0,120}\bPFAS\b",
        r"\bpyrolysis of "
        r"(?:PFAS|PFAS-containing|PFAS-contaminated)\b",
        r"\bPFAS (?:destruction|degradation|treatment) "
        r"(?:by|using|via) pyrolysis\b",
        r"\bpyrolytic "
        r"(?:destruction|degradation|treatment) of PFAS\b",
        r"\bPFAS-contaminated .{0,60}\bpyrolysis\b",
        r"\bPFAS.{0,120}\bincineration\b",
        r"\bincineration\b.{0,120}\bPFAS\b",
        r"\bPFAS.{0,120}\binduction heating\b",
        r"\binduction heating\b.{0,120}\bPFAS\b",
    ],
    "biological": [
        r"\bbiodegradation\b",
        r"\bbiological degradation\b",
        r"\bmicrobial degradation\b",
        r"\bbioremediation\b",
    ],
    "capture_and_destroy": [
        r"\bcapture[- ]and[- ]destroy\b",
        r"\bcombined adsorption and electrochemical oxidation\b",
        r"\bfoam fractionation "
        r"(?:combined with|followed by|coupled with) "
        r"(?:electrochemical oxidation|plasma|destruction)\b",
        r"\badsorption "
        r"(?:combined with|followed by|coupled with) "
        r"(?:electrochemical oxidation|plasma|destruction)\b",
        r"\bion exchange "
        r"(?:combined with|followed by|coupled with) "
        r"(?:electrochemical oxidation|plasma|destruction)\b",
        r"\bmembrane concentrate(?:s)? "
        r"(?:treated by|treated with|followed by|coupled with) "
        r"(?:electrochemical oxidation|plasma|hydrothermal|destruction)\b",
        r"\bregeneration solution(?:s)? "
        r"(?:treated by|treated with|followed by|coupled with) "
        r"(?:electrochemical oxidation|plasma|destruction)\b",
    ],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into dictionaries."""
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def matches_any(text: str, patterns: list[str]) -> bool:
    """Return True when any regular-expression pattern matches."""
    return any(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        for pattern in patterns
    )


def classify_text(title: str, abstract: str) -> list[str]:
    """Assign one or more technology labels from title and abstract."""
    text = f"{title}\n{abstract}".strip()
    labels = []

    for technology, patterns in TECHNOLOGY_RULES.items():
        if matches_any(text, patterns):
            labels.append(technology)

    return sorted(labels)


def classify_records(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Add rule-based technology labels to every record."""
    classified = []

    for row in rows:
        labels = classify_text(
            row.get("title", ""),
            row.get("abstract", ""),
        )

        enriched = dict(row)
        enriched["technology_count"] = len(labels)
        enriched["technology_labels"] = ";".join(labels)
        enriched["classification_method"] = "title_abstract_rules"
        classified.append(enriched)

    return classified


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    """Write classified records to CSV."""
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
            "Apply initial rule-based technology classification "
            "to deduplicated OpenAlex records."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/processed/openalex_deduplicated.csv"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "data/processed/openalex_classified.csv"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows = read_csv(args.input)
    classified = classify_records(rows)
    write_csv(classified, args.output)

    classified_count = sum(
        bool(row["technology_labels"])
        for row in classified
    )

    multi_label_count = sum(
        int(row["technology_count"]) > 1
        for row in classified
    )

    print(f"Input records: {len(rows)}")
    print(f"Records with at least one label: {classified_count}")
    print(
        "Records without a technology label: "
        f"{len(rows) - classified_count}"
    )
    print(f"Records with multiple labels: {multi_label_count}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()