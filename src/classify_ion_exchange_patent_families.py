from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_family_summary.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_family_intelligence.csv"
)


def classify_family(title: str) -> dict[str, str]:
    """Assign preliminary intelligence labels from the family title."""

    text = title.lower()

    treatment_mode = "adsorption"

    if "regenerat" in text:
        treatment_mode = "regeneration"
    elif "mineralization" in text or "degradation" in text:
        treatment_mode = "capture_and_destroy"
    elif "advanced oxidation" in text:
        treatment_mode = "combined_process"

    resin_strategy = "ion_exchange_resin"

    if "selective" in text:
        resin_strategy = "selective_resin"
    elif "functionalized" in text or "modified" in text:
        resin_strategy = "functionalized_resin"
    elif "dimethylethanolamine" in text:
        resin_strategy = "amine_resin"

    return {
        "treatment_mode": treatment_mode,
        "resin_strategy": resin_strategy,
    }

def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Family summary file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    labels = df[
        "representative_title"
    ].fillna("").apply(classify_family)

    labels_df = pd.DataFrame(
        labels.tolist()
    )

    result = pd.concat(
        [
            df.reset_index(drop=True),
            labels_df,
        ],
        axis=1,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Families classified: {len(result)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nTreatment mode:")
    print(
        result["treatment_mode"]
        .value_counts()
        .to_string()
    )

    print("\nResin strategy:")
    print(
        result["resin_strategy"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()

