from __future__ import annotations

import csv
from pathlib import Path


INPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_screening.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_auto_screened.csv"
)

PFAS_TERMS = (
    "pfas",
    "pfoa",
    "pfos",
    "perfluoroalkyl",
    "polyfluoroalkyl",
    "perfluorinated",
    "polyfluorinated",
)

WATER_TERMS = (
    "water",
    "groundwater",
    "wastewater",
    "aqueous",
    "leachate",
    "effluent",
)

ACTIVATED_CARBON_TERMS = (
    "activated carbon",
    "granular activated carbon",
    "powdered activated carbon",
    "gac",
    "pac",
)

def read_screening_rows() -> list[dict[str, str]]:
    """Read the adsorption patent-screening dataset."""
    with INPUT_PATH.open(
        encoding="utf-8",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def normalize_title(
    row: dict[str, str],
) -> str:
    """Return a lowercase normalized patent title."""
    return " ".join(
        row.get(
            "title",
            "",
        ).lower().split()
    )

def contains_any(
    text: str,
    terms: tuple[str, ...],
    ) -> bool:
    """Return True when text contains any supplied term."""
    return any(
        term in text
        for term in terms
)


def classify_title(
    title: str,
) -> tuple[str, str]:
    """Assign a conservative title-level screening decision."""
    has_pfas = contains_any(
        title,
        PFAS_TERMS,
    )
    has_water = contains_any(
        title,
        WATER_TERMS,
    )
    has_activated_carbon = contains_any(
        title,
        ACTIVATED_CARBON_TERMS,
    )

    if (
        has_pfas
        and has_water
        and has_activated_carbon
    ):
        return (
            "include",
            (
                "Title explicitly links PFAS, an aqueous "
                "stream and activated-carbon treatment."
            ),
        )

    if (
        has_pfas
        and has_activated_carbon
    ):
        return (
            "context_only",
            (
                "Title links PFAS and activated carbon, "
                "but aqueous treatment is not explicit."
            ),
        )

    if (
        has_water
        and has_activated_carbon
        and not has_pfas
    ):
        return (
            "uncertain",
            (
                "Title describes activated-carbon water "
                "treatment, but PFAS relevance is not explicit."
            ),
        )

    return (
        "uncertain",
        (
            "Title alone does not provide enough evidence "
            "for a confident relevance decision."
        ),
    )

def apply_title_screening(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Apply conservative title-level screening rules."""
    screened_rows: list[dict[str, str]] = []

    for row in rows:
        title = normalize_title(row)

        decision, note = classify_title(
            title
        )

        updated_row = dict(row)

        updated_row[
            "manual_relevance_decision"
        ] = decision

        updated_row[
            "manual_screening_notes"
        ] = note

        screened_rows.append(
            updated_row
        )

    return screened_rows

def write_screened_csv(
    rows: list[dict[str, str]],
) -> Path:
    """Write the title-screened adsorption patent dataset."""
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not rows:
        raise ValueError(
            "No patent records available for screening."
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

def print_screening_summary(
    rows: list[dict[str, str]],
) -> None:
    """Print counts for the automatic screening decisions."""
    counts: dict[str, int] = {}

    for row in rows:
        decision = row.get(
            "manual_relevance_decision",
            "",
        ).strip() or "blank"

        counts[decision] = (
            counts.get(decision, 0)
            + 1
        )

    print(
        f"Patent records screened: {len(rows)}"
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
    """Automatically screen adsorption patent titles."""
    rows = read_screening_rows()

    screened_rows = apply_title_screening(
        rows
    )

    output_path = write_screened_csv(
        screened_rows
    )

    print_screening_summary(
        screened_rows
    )

    print(
        f"Output written to: {output_path}"
    )


if __name__ == "__main__":
    main()
    