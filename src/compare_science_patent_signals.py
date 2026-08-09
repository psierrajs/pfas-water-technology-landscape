from __future__ import annotations

from pathlib import Path

import pandas as pd


SCIENCE_PATH = Path(
    "data/processed/openalex_classified.csv"
)

PATENT_PATH = Path(
    "data/processed/patents/"
    "patent_technology_comparison.csv"
)

OUTPUT_PATH = Path(
    "data/processed/"
    "science_patent_technology_comparison.csv"
)


ACTIVATED_CARBON_TERMS = (
    "activated carbon",
    "granular activated carbon",
    "powdered activated carbon",
    " gac ",
    " pac ",
)


def has_technology(
    labels: str,
    technology: str,
) -> bool:
    values = {
        value.strip()
        for value in str(labels).split(";")
    }

    return technology in values

def build_science_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    science = df.copy()

    text = (
        science["title"].fillna("")
        + " "
        + science["abstract"].fillna("")
    ).str.lower()

    has_adsorption = science[
        "technology_labels"
    ].fillna("").apply(
        lambda value: has_technology(
            value,
            "adsorption",
        )
    )

    has_activated_carbon = text.apply(
        lambda value: any(
            term in value
            for term in ACTIVATED_CARBON_TERMS
        )
    )

    has_ion_exchange = science[
        "technology_labels"
    ].fillna("").apply(
        lambda value: has_technology(
            value,
            "ion_exchange",
        )
    )

    records = [
        {
            "technology": "activated_carbon",
            "science_publications": int(
                (has_adsorption & has_activated_carbon).sum()
            ),
        },
        {
            "technology": "ion_exchange",
            "science_publications": int(
                has_ion_exchange.sum()
            ),
        },
    ]

    return pd.DataFrame(records)

def build_patent_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    patent_counts = (
        df["technology"]
        .value_counts()
        .rename_axis("technology")
        .reset_index(name="patent_families")
    )

    return patent_counts

def main() -> None:
    if not SCIENCE_PATH.exists():
        raise FileNotFoundError(
            f"Science dataset not found: {SCIENCE_PATH}"
        )

    if not PATENT_PATH.exists():
        raise FileNotFoundError(
            f"Patent comparison dataset not found: {PATENT_PATH}"
        )

    science_df = pd.read_csv(SCIENCE_PATH)
    patent_df = pd.read_csv(PATENT_PATH)

    science_summary = build_science_summary(
        science_df
    )

    patent_summary = build_patent_summary(
        patent_df
    )

    comparison = science_summary.merge(
        patent_summary,
        on="technology",
        how="left",
    )

    comparison["patent_families"] = (
        comparison["patent_families"]
        .fillna(0)
        .astype(int)
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparison.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("Science ↔ patent comparison:")
    print(
        comparison.to_string(
            index=False,
        )
    )

    print(f"\nOutput: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    