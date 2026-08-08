from __future__ import annotations

from pathlib import Path

import pandas as pd


RAW_PATH = Path(
    "data/raw/patents/"
    "pat_ix_001_patentscope.xls"
)

PROCESSED_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_processed.csv"
)

QUERY_ID = "PAT-IX-001"
TECHNOLOGY_LABEL = "ion_exchange"


def load_patentscope_export() -> pd.DataFrame:
    """Load the PATENTSCOPE XLS export."""

    df = pd.read_excel(
        RAW_PATH,
        header=5,
    )

    return df


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"PATENTSCOPE export not found: {RAW_PATH}"
        )

    df = load_patentscope_export()

    processed = pd.DataFrame(
        {
            "query_id": QUERY_ID,
            "technology": TECHNOLOGY_LABEL,
            "application_id": df["Application Id"].astype(str),
            "application_number": df["Application Number"].astype(str),
            "application_date": pd.to_datetime(
                df["Application Date"],
                format="%d.%m.%Y",
                errors="coerce",
            ),
            "country": df["Country"].astype(str),
            "title": df["Title"].astype(str).str.strip(),
            "ipc": df["I P C"].astype(str).str.strip(),
        }
    )

    PROCESSED_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed.to_csv(
        PROCESSED_PATH,
        index=False,
    )

    print(f"Records processed: {len(processed)}")
    print(f"Output: {PROCESSED_PATH}")

    print("\nDate range:")
    print(
        processed["application_date"].min(),
        "to",
        processed["application_date"].max(),
    )

    print("\nCountries:")
    print(
        processed["country"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()