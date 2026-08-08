from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_initial_screening.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_uncertain_review.csv"
)


REVIEW_DECISIONS = {
    "WO2025212369": (
        "include",
        "PFAS-loaded ion-exchange resin regeneration; directly relevant."
    ),
    "WO2009125695": (
        "exclude",
        "Fluorinated ion-exchange resin composition associated with "
        "electrochemical/fuel-cell applications."
    ),
    "WO2022212165": (
        "context_only",
        "PFAS separation from water; ion-exchange relevance plausible "
        "but not explicit in title."
    ),
    "CN401483931": (
        "exclude",
        "Ion-exchange membrane material rather than PFAS water treatment."
    ),
    "CN362133082": (
        "context_only",
        "PFAS water purification system, but ion exchange is not explicit "
        "in title or IPC."
    ),
    "JP271198214": (
        "context_only",
        "Recovery of fluorinated emulsifier using ion-exchange treatment; "
        "useful historical context."
    ),
    "JP268502667": (
        "exclude",
        "Ion-exchange membrane associated with electrochemical applications."
    ),
    "WO2026146391": (
        "include",
        "Modified ion-exchange resin with water-treatment and PFAS-related IPC."
    ),
}

REVIEW_DECISIONS.update(
    {
        "JP269862938": (
            "exclude",
            "Ion-exchange composite membrane associated with "
            "electrochemical applications rather than PFAS water treatment."
        ),
        "US350349212": (
            "context_only",
            "PFAS filtration technology; possible ion-exchange component "
            "but not explicit in the title."
        ),
        "WO2025106791": (
            "exclude",
            "PFAS adsorption and destruction technology without clear "
            "ion-exchange resin relevance."
        ),
        "CN416016137": (
            "exclude",
            "Ion-exchange membrane material rather than PFAS water treatment."
        ),
        "WO2022115429": (
            "context_only",
            "Water-treatment patent with ion-exchange IPC classification; "
            "PFAS relevance requires further confirmation."
        ),
        "CN447747737": (
            "exclude",
            "Analytical detection of perfluoroalkyl substances rather than "
            "water treatment."
        ),
        "JP474963943": (
            "context_only",
            "Groundwater purification using ion-exchange-related treatment; "
            "PFAS relevance requires further confirmation."
        ),
        "US36656992": (
            "exclude",
            "Fluorinated chemical synthesis unrelated to PFAS water treatment."
        ),
        "US73153728": (
            "exclude",
            "Fuel-cell electrolyte and membrane technology."
        ),
    }
)

def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Initial screening file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    review = df[
        df["screening_decision"] == "uncertain"
    ].copy()

    review["review_decision"] = review[
        "application_id"
    ].map(
        lambda value: REVIEW_DECISIONS.get(
            value,
            ("uncertain", "Requires manual review."),
        )[0]
    )

    review["review_note"] = review[
        "application_id"
    ].map(
        lambda value: REVIEW_DECISIONS.get(
            value,
            ("uncertain", "Requires manual review."),
        )[1]
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    review.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Records reviewed: {len(review)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nReview decisions:")
    print(
        review["review_decision"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()
