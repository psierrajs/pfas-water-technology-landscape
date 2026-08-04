from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


INPUT_PATH = Path(
    "data/processed/evidence_technology_matrix/"
    "evidence_type_by_technology.csv"
)

OUTPUT_DIR = Path(
    "data/processed/technology_maturity"
)

OUTPUT_PATH = (
    OUTPUT_DIR
    / "technology_maturity_scores.csv"
)

EVIDENCE_WEIGHTS = {
    "field_demonstration": 8.0,
    "pilot": 5.0,
    "life_cycle_assessment": 3.0,
    "experimental": 2.0,
    "mechanistic": 1.5,
    "computational": 1.0,
}

DEPLOYMENT_WEIGHTS = {
    "field_demonstration": 8.0,
    "pilot": 5.0,
    "life_cycle_assessment": 3.0,
}

RESEARCH_WEIGHTS = {
    "experimental": 2.0,
    "mechanistic": 1.5,
    "computational": 1.0,
}

def read_matrix_rows() -> list[dict[str, str]]:
    """Read the evidence-by-technology matrix."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def to_int(
    row: dict[str, str],
    field: str,
) -> int:
    """Convert a matrix value to an integer."""
    value = row.get(field, "").strip()

    if not value:
        return 0

    return int(value)

def calculate_raw_score(
    row: dict[str, str],
) -> float:
    """Calculate the weighted maturity evidence score."""
    score = 0.0

    for evidence_type, weight in EVIDENCE_WEIGHTS.items():
        score += (
            to_int(row, evidence_type)
            * weight
        )

    return score
def calculate_weighted_score(
    row: dict[str, str],
    weights: dict[str, float],
) -> float:
    """Calculate a score using a selected weight set."""
    score = 0.0

    for evidence_type, weight in weights.items():
        score += (
            to_int(row, evidence_type)
            * weight
        )

    return score

def calculate_normalized_score(
    raw_score: float,
    total_publications: int,
) -> float:
    """Normalize maturity evidence by publication volume."""
    if total_publications == 0:
        return 0.0

    return (
        raw_score
        / total_publications
        * 100
    )
def build_maturity_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Create maturity-score rows for each technology."""
    output_rows: list[dict[str, Any]] = []

    for row in rows:
        total_publications = to_int(
            row,
            "total_unique_publications",
        )

        raw_score = calculate_raw_score(
            row
        )
        deployment_score = calculate_weighted_score(
            row,
            DEPLOYMENT_WEIGHTS,
        )

        research_score = calculate_weighted_score(
            row,
            RESEARCH_WEIGHTS,
        )

        normalized_deployment_score = (
            calculate_normalized_score(
                deployment_score,
                total_publications,
            )
        )

        normalized_research_score = (
            calculate_normalized_score(
                research_score,
                total_publications,
            )
        )
        normalized_score = (
            calculate_normalized_score(
                raw_score,
                total_publications,
            )
        )

        output_rows.append(
            {
                "technology": row["technology"],
                "total_unique_publications": (
                    total_publications
                ),
                "raw_maturity_score": round(
                    raw_score,
                    2,
                ),
                "normalized_maturity_score": round(
                    normalized_score,
                    2,
                ),
                "deployment_score": round(
                    deployment_score,
                    2,
                ),
                "normalized_deployment_score": round(
                    normalized_deployment_score,
                    2,
                ),
                "research_score": round(
                    research_score,
                    2,
                ),
                "normalized_research_score": round(
                    normalized_research_score,
                    2,
                ),
                "field_demonstration": to_int(
                    row,
                    "field_demonstration",
                ),
                "pilot": to_int(
                    row,
                    "pilot",
                ),
                "life_cycle_assessment": to_int(
                    row,
                    "life_cycle_assessment",
                ),
                "experimental": to_int(
                    row,
                    "experimental",
                ),
                "mechanistic": to_int(
                    row,
                    "mechanistic",
                ),
                "computational": to_int(
                    row,
                    "computational",
                ),
            }
        )

    return output_rows

def sort_maturity_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort technologies by normalized and raw maturity."""
    return sorted(
        rows,
        key=lambda row: (
            row["normalized_maturity_score"],
            row["raw_maturity_score"],
            row["total_unique_publications"],
            row["technology"],
        ),
        reverse=True,
    )


def write_maturity_csv(
    rows: list[dict[str, Any]],
) -> Path:
    """Write the technology maturity scores."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "technology",
        "total_unique_publications",
        "raw_maturity_score",
        "normalized_maturity_score",
        "deployment_score",
        "normalized_deployment_score",
        "research_score",
        "normalized_research_score",
        "field_demonstration",
        "pilot",
        "life_cycle_assessment",
        "experimental",
        "mechanistic",
        "computational",
    ]

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

def print_maturity_summary(
    rows: list[dict[str, Any]],
) -> None:
    """Print the ranked technology maturity scores."""
    print(
        "\nTechnology maturity scores"
    )
    print("-" * 150)

    for rank, row in enumerate(
        rows,
        start=1,
    ):
        print(
            f"{rank:>2}. "
            f"{row['normalized_maturity_score']:>6.2f} overall | "
            f"{row['normalized_deployment_score']:>6.2f} deployment | "
            f"{row['normalized_research_score']:>6.2f} research | "
            f"{row['raw_maturity_score']:>6.2f} raw | "
            f"{row['total_unique_publications']:>3} publications | "
            f"{row['technology']}"
        )

def main() -> None:
    """Calculate and export technology maturity scores."""
    matrix_rows = read_matrix_rows()

    maturity_rows = build_maturity_rows(
        matrix_rows
    )

    maturity_rows = sort_maturity_rows(
        maturity_rows
    )

    output_path = write_maturity_csv(
        maturity_rows
    )

    print(
        f"Technologies scored: {len(maturity_rows)}"
    )
    print(
        f"Output written to: {output_path}"
    )

    print_maturity_summary(
        maturity_rows
    )


if __name__ == "__main__":
    main()

