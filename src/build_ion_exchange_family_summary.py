from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_consolidated_screening.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_family_summary.csv"
)


def normalize_title(title: str) -> str:
    """Normalize patent titles for provisional grouping."""

    text = title.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    return " ".join(
        text.split()
    )

def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Consolidated screening file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    included = df[
        df["final_decision"] == "include"
    ].copy()

    included["title_normalized"] = (
        included["title"]
        .fillna("")
        .apply(normalize_title)
    )

    included["family_group_key"] = (
        included["title_normalized"]
    )

    family_ids = {}
    next_family_number = 1

    for key in included["family_group_key"]:
        if key not in family_ids:
            family_ids[key] = (
                f"FAM-IX-{next_family_number:03d}"
            )
            next_family_number += 1

    included["family_id"] = (
        included["family_group_key"]
        .map(family_ids)
    )

    family_summary = (
        included.groupby("family_id")
        .agg(
            publication_count=(
                "application_id",
                "count",
            ),
            representative_application=(
                "application_id",
                "first",
            ),
            representative_title=(
                "title",
                "first",
            ),
            countries=(
                "country",
                lambda values: "; ".join(
                    sorted(set(values))
                ),
            ),
            earliest_application_date=(
                "application_date",
                "min",
            ),
        )
        .reset_index()
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    family_summary.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"Included publications: "
        f"{len(included)}"
    )

    print(
        f"Provisional families: "
        f"{len(family_summary)}"
    )

    print(
        f"Multi-publication families: "
        f"{(family_summary['publication_count'] > 1).sum()}"
    )

    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
