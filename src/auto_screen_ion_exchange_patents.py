from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_processed.csv"
)

OUTPUT_PATH = Path(
    "data/processed/patents/pat_ix_001/"
    "pat_ix_001_initial_screening.csv"
)


PFAS_TERMS = (
    "pfas",
    "pfoa",
    "pfos",
    "perfluoroalkyl",
    "polyfluoroalkyl",
    "per- and polyfluoroalkyl",
    "per-and polyfluoroalkyl",
)

ION_EXCHANGE_TERMS = (
    "ion exchange",
    "ion-exchange",
    "anion exchange",
    "anion-exchange",
    "exchange resin",
    "exchange resins",
)

WATER_TERMS = (
    "water",
    "groundwater",
    "wastewater",
    "leachate",
    "aqueous",
)

PFAS_IPC_TERMS = (
    "C02F 101/36",
)

WATER_TREATMENT_IPC_PREFIXES = (
    "C02F",
)

ION_EXCHANGE_IPC_TERMS = (
    "C02F 1/42",
    "B01J 41/",
    "B01J 49/",
    "B01D 15/36",
)


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text.lower() for term in terms)

def classify_record(row: pd.Series) -> str:
    """Classify a patent using title and IPC evidence."""

    title = str(row.get("title", "")).lower()
    ipc = str(row.get("ipc", "")).lower()

    has_pfas_title = has_any(
        title,
        PFAS_TERMS,
    )

    has_ion_exchange_title = has_any(
        title,
        ION_EXCHANGE_TERMS,
    )

    has_water_title = has_any(
        title,
        WATER_TERMS,
    )

    has_pfas_ipc = has_any(
        ipc,
        PFAS_IPC_TERMS,
    )

    has_water_ipc = any(
        prefix.lower() in ipc
        for prefix in WATER_TREATMENT_IPC_PREFIXES
    )

    has_ion_exchange_ipc = has_any(
        ipc,
        ION_EXCHANGE_IPC_TERMS,
    )

    if (
        (has_pfas_title or has_pfas_ipc)
        and
        (has_ion_exchange_title or has_ion_exchange_ipc)
        and
        (has_water_title or has_water_ipc)
    ):
        return "include"

    if (
        (has_pfas_title or has_pfas_ipc)
        and
        (has_ion_exchange_title or has_ion_exchange_ipc)
    ):
        return "context_only"

    if (
        has_pfas_title
        or has_pfas_ipc
        or has_ion_exchange_title
        or has_ion_exchange_ipc
    ):
        return "uncertain"

    return "exclude"

def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Processed patent file not found: {INPUT_PATH}"
        )

    df = pd.read_csv(INPUT_PATH)

    df["screening_decision"] = df.apply(
        classify_record,
        axis=1,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"Records screened: {len(df)}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nScreening decisions:")
    print(
        df["screening_decision"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    main()
