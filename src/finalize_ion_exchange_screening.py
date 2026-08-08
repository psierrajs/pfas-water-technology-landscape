from __future__ import annotations

from pathlib import Path

import pandas as pd


INITIAL_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_initial_screening.csv"
)

REVIEW_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_uncertain_review.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_consolidated_screening.csv"
)
QA_OVERRIDES = {
    "WO2025006915": (
        "include",
        "Verified hybrid PFAS degradation system using an ion-exchange "
        "resin as catalyst support."
    ),
    "WO2026102479": (
        "include",
        "Strong ion-exchange and PFAS water-treatment IPC evidence."
    ),
    "US395388231": (
        "context_only",
        "Soil-remediation invention with ion-exchange/water-treatment "
        "elements; not primarily a PFAS water-treatment resin invention."
    ),
}

def main() -> None:
    if not INITIAL_PATH.exists():
        raise FileNotFoundError(
            f"Initial screening file not found: {INITIAL_PATH}"
        )

    if not REVIEW_PATH.exists():
        raise FileNotFoundError(
            f"Review file not found: {REVIEW_PATH}"
        )

    initial = pd.read_csv(INITIAL_PATH)
    review = pd.read_csv(REVIEW_PATH)

    review_map = review.set_index(
        "application_id"
    )[
        [
            "review_decision",
            "review_note",
        ]
    ].to_dict("index")

    final_decisions = []
    final_notes = []

    for _, row in initial.iterrows():
        application_id = row["application_id"]
        initial_decision = row["screening_decision"]

        if initial_decision == "uncertain":
            review_entry = review_map.get(application_id)

            if review_entry is None:
                final_decisions.append("uncertain")
                final_notes.append(
                    "No review decision available."
                )
            else:
                final_decisions.append(
                    review_entry["review_decision"]
                )
                final_notes.append(
                    review_entry["review_note"]
                )
        else:
            final_decisions.append(initial_decision)
            final_notes.append(
                "Retained from automated screening."
            )

    initial["final_decision"] = final_decisions
    initial["final_note"] = final_notes

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    for application_id, (decision, note) in QA_OVERRIDES.items():
        mask = initial["application_id"] == application_id
        initial.loc[mask, "final_decision"] = decision
        initial.loc[mask, "final_note"] = note
        initial.to_csv(
            OUTPUT_PATH,
            index=False,
        )

    print(f"Records consolidated: {len(initial)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nFinal decisions:")
    print(
        initial["final_decision"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()

