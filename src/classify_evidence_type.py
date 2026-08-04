from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/openalex_analysis_corpus.csv"
)

OUTPUT_DIR = Path(
    "data/processed/evidence_type"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "openalex_evidence_type_classified.csv"
)

PRIMARY_TIERS = {
    "core",
    "secondary",
    "manual_review",
}

EVIDENCE_TYPES = (
    "field_demonstration",
    "pilot",
    "techno_economic",
    "life_cycle_assessment",
    "review",
    "computational",
    "mechanistic",
    "experimental",
    "laboratory",
    "other",
)

EVIDENCE_PATTERNS = {
    "field_demonstration": (
        r"\bfield demonstration\b",
        r"\bfield trial\b",
        r"\bfield-scale\b",
        r"\bfull-scale\b",
        r"\bsite demonstration\b",
    ),
    "pilot": (
        r"\bpilot-scale\b",
        r"\bpilot scale\b",
        r"\bpilot treatment\b",
        r"\bpilot plant\b",
        r"\bdemonstration-scale\b",
    ),
    "techno_economic": (
        r"\btechno-economic\b",
        r"\btechnoeconomic\b",
        r"\bcost analysis\b",
        r"\beconomic assessment\b",
        r"\bcost evaluation\b",
    ),
    "life_cycle_assessment": (
        r"\blife cycle assessment\b",
        r"\blife-cycle assessment\b",
        r"\bLCA\b",
        r"\benvironmental footprint\b",
    ),
    "review": (
        r"\breview\b",
        r"\bmeta-analysis\b",
        r"\bstate of the art\b",
        r"\bstate-of-the-art\b",
        r"\bstate of the science\b",
        r"\bstate-of-the-science\b",
        r"\bcritical assessment\b",
        r"\bperspective\b",
        r"\brecent progress\b",
        r"\brecent advances\b",
        r"\boverview\b",
        r"\btechnology status\b",
        r"\bcurrent status\b",
        r"\bchallenges and current status\b",
        r"\bchallenges and opportunities\b",
        r"\binsights into\b",
        r"\bprogress and perspectives\b",
        r"\bresearch updates\b",
        r"\bemerging .* technologies\b",
        r"\bfuture perspectives\b",
    ),
    "computational": (
        r"\bsimulation\b",
        r"\bmolecular dynamics\b",
        r"\bfirst-principles\b",
        r"\bDFT\b",
        r"\bdensity functional theory\b",
        r"\bmachine learning\b",
        r"\bin silico\b",
        r"\btheoretical evaluation\b",
        r"\bkinetic model\b",
        r"\bmodelling study\b",
        r"\bmodeling study\b",
    ),  
    "mechanistic": (
        r"\bmechanism\b",
        r"\bmechanistic\b",
        r"\bpathway\b",
        r"\bkinetic\b",
        r"\bDFT\b",
        r"\bdensity functional theory\b",
        r"\breaction intermediates\b",
    ),
    "laboratory": (
        r"\bbatch experiment\b",
        r"\bbatch reactor\b",
        r"\blaboratory-scale\b",
        r"\blab-scale\b",
        r"\bbench-scale\b",
        r"\bcolumn experiment\b",
        r"\bsynthetic water\b",
        r"\baqueous solution\b",
    ),
    "experimental": (
        r"\bvalidation of\b",
        r"\bperformance testing\b",
        r"\bperformance evaluation\b",
        r"\bexperimental study\b",
        r"\bexperimental investigation\b",
        r"\bexperiments?\b",
        r"\breactor\b",
        r"\banode\b",
        r"\belectrode\b",
        r"\bphotocatalytic degradation\b",
        r"\belectrochemical degradation\b",
        r"\bplasma degradation\b",
        r"\badsorption onto\b",
        r"\badsorption by\b",
        r"\bremoval using\b",
        r"\bdegradation using\b",
    ),
}

def normalize_text(
    title: str,
    abstract: str,
) -> str:
    """Combine and normalize searchable publication text."""
    combined = f"{title} {abstract}"

    return re.sub(
        r"\s+",
        " ",
        combined,
    ).strip()


def match_patterns(
    text: str,
    patterns: tuple[str, ...],
) -> list[str]:
    """Return regex patterns matched in the text."""
    return [
        pattern
        for pattern in patterns
        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
    ]


def classify_evidence(
    title: str,
    abstract: str,
) -> dict[str, Any]:
    """Assign evidence types using title-first rules."""
    title_text = normalize_text(
        title,
        "",
    )
    full_text = normalize_text(
        title,
        abstract,
    )

    title_matches: dict[str, list[str]] = {}
    full_matches: dict[str, list[str]] = {}

    for evidence_type in EVIDENCE_TYPES:
        if evidence_type == "other":
            continue

        patterns = EVIDENCE_PATTERNS.get(
            evidence_type,
            (),
        )

        title_matches[evidence_type] = match_patterns(
            title_text,
            patterns,
        )

        full_matches[evidence_type] = match_patterns(
            full_text,
            patterns,
        )

    title_priority = (
        "review",
        "life_cycle_assessment",
        "techno_economic",
        "field_demonstration",
        "pilot",
        "computational",
        "mechanistic",
        "experimental",
        "laboratory",
    )

    primary_type = "other"

    for evidence_type in title_priority:
        if title_matches[evidence_type]:
            primary_type = evidence_type
            break

    matched_types = [
        evidence_type
        for evidence_type in EVIDENCE_TYPES
        if (
            evidence_type != "other"
            and full_matches.get(evidence_type)
        )
    ]

    matched_patterns = [
        f"{evidence_type}:{pattern}"
        for evidence_type in matched_types
        for pattern in full_matches[evidence_type]
    ]

    return {
        "primary_evidence_type": primary_type,
        "evidence_types": "|".join(
            matched_types
        ),
        "evidence_type_count": len(
            matched_types
        ),
        "evidence_signals": "|".join(
            matched_patterns
        ),
        "evidence_method": "rule_based_v3_title_primary",
    }

def read_corpus_rows() -> list[dict[str, str]]:
    """Read the analysis corpus."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def classify_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Classify evidence type for primary-tier publications."""
    classified_rows: list[dict[str, Any]] = []

    for row in rows:
        tier = row.get(
            "analysis_tier",
            "",
        ).strip()

        if tier not in PRIMARY_TIERS:
            continue

        evidence = classify_evidence(
            row.get("title", ""),
            row.get("abstract", ""),
        )

        classified_rows.append(
            {
                **row,
                **evidence,
            }
        )

    return classified_rows

def write_classified_csv(
    rows: list[dict[str, Any]],
) -> Path:
    """Write the evidence-type classified corpus."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No classified rows were generated."
        )

    fieldnames = list(rows[0].keys())

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


def summarize_evidence_types(
    rows: list[dict[str, Any]],
) -> dict[str, int]:
    """Count publications by primary evidence type."""
    counts = {
        evidence_type: 0
        for evidence_type in EVIDENCE_TYPES
    }

    for row in rows:
        evidence_type = row[
            "primary_evidence_type"
        ]
        counts[evidence_type] += 1

    return counts


def print_summary(
    rows: list[dict[str, Any]],
) -> None:
    """Print evidence-type classification totals."""
    counts = summarize_evidence_types(rows)

    print(
        f"Publications classified: {len(rows)}"
    )
    print("\nPrimary evidence types")
    print("-" * 50)

    for evidence_type, count in sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(
            f"{count:>4} | {evidence_type}"
        )

def main() -> None:
    """Classify publication evidence types."""
    rows = read_corpus_rows()

    classified_rows = classify_rows(rows)

    output_path = write_classified_csv(
        classified_rows
    )

    print(
        f"Corpus rows read: {len(rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )

    print_summary(
        classified_rows
    )


if __name__ == "__main__":
    main()
