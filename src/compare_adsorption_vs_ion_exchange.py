from __future__ import annotations

from pathlib import Path

import pandas as pd


ADSORPTION_PATH = Path(
    "data/processed/patents/pat_ads_001a/"
    "pat_ads_001a_family_intelligence_final.csv"
)

ION_EXCHANGE_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_family_intelligence.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/"
    "patent_technology_comparison.csv"
)

def load_adsorption() -> pd.DataFrame:
    df = pd.read_csv(ADSORPTION_PATH).copy()

    result = pd.DataFrame(
        {
            "technology": "activated_carbon",
            "family_id": df["family_group"],
            "treatment_mode": df["treatment_mode"],
            "strategic_theme": df["strategic_theme"],
            "maturity_signal": df["maturity_signal"],
        }
    )

    return result


def load_ion_exchange() -> pd.DataFrame:
    df = pd.read_csv(ION_EXCHANGE_PATH).copy()

    result = pd.DataFrame(
        {
            "technology": "ion_exchange",
            "family_id": df["family_id"],
            "treatment_mode": df["treatment_mode"],
            "strategic_theme": df["resin_strategy"],
            "maturity_signal": "not_classified",
        }
    )

    return result

def main() -> None:
    adsorption = load_adsorption()
    ion_exchange = load_ion_exchange()

    combined = pd.concat(
        [
            adsorption,
            ion_exchange,
        ],
        ignore_index=True,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    combined.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Combined patent families: {len(combined)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nFamilies by technology:")
    print(
        combined["technology"]
        .value_counts()
        .to_string()
    )

    print("\nTreatment mode by technology:")
    print(
        pd.crosstab(
            combined["technology"],
            combined["treatment_mode"],
        ).to_string()
    )


if __name__ == "__main__":
    main()
    