from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

ORGANIZATIONS_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "commercial_intelligence"
    / "organizations.csv"
)

SIGNALS_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "commercial_intelligence"
    / "commercial-signals.csv"
)


REQUIRED_ORGANIZATION_FIELDS = [
    "organization_id",
    "organization_name",
    "normalized_name",
    "organization_type",
    "technology_labels",
    "technology_origin_role",
    "commercialization_entity",
]


REQUIRED_SIGNAL_FIELDS = [
    "signal_id",
    "organization_id",
    "organization_name",
    "evidence_type",
    "technology_labels",
    "treatment_role",
    "maturity_or_deployment_stage",
    "source_title",
    "source_url",
    "confidence_level",
    "verification_status",
]


def find_empty_required_fields(df, fields, label):
    problems = []

    for field in fields:
        if field not in df.columns:
            problems.append(
                f"{label}: missing required column '{field}'"
            )
            continue

        empty = df[
            df[field].isna()
            | (df[field].astype(str).str.strip() == "")
        ]

        for index in empty.index:
            problems.append(
                f"{label}: row {index + 2} has empty '{field}'"
            )

    return problems


def main():
    organizations = pd.read_csv(ORGANIZATIONS_INPUT)
    signals = pd.read_csv(SIGNALS_INPUT)

    problems = []

    duplicate_org_ids = organizations[
        organizations["organization_id"].duplicated(
            keep=False
        )
    ]

    if not duplicate_org_ids.empty:
        for value in sorted(
            duplicate_org_ids["organization_id"].unique()
        ):
            problems.append(
                f"Duplicate organization_id: {value}"
            )

    duplicate_signal_ids = signals[
        signals["signal_id"].duplicated(
            keep=False
        )
    ]

    if not duplicate_signal_ids.empty:
        for value in sorted(
            duplicate_signal_ids["signal_id"].unique()
        ):
            problems.append(
                f"Duplicate signal_id: {value}"
            )

    organization_ids = set(
        organizations["organization_id"].dropna()
    )

    unknown_org_signals = signals[
        ~signals["organization_id"].isin(
            organization_ids
        )
    ]

    for _, row in unknown_org_signals.iterrows():
        problems.append(
            f"Signal {row['signal_id']} references unknown "
            f"organization_id {row['organization_id']}"
        )

    problems.extend(
        find_empty_required_fields(
            organizations,
            REQUIRED_ORGANIZATION_FIELDS,
            "Organization",
        )
    )

    problems.extend(
        find_empty_required_fields(
            signals,
            REQUIRED_SIGNAL_FIELDS,
            "Signal",
        )
    )

    print(
        f"Organizations checked: {len(organizations)}"
    )

    print(
        f"Commercial signals checked: {len(signals)}"
    )

    print()

    if problems:
        print(
            f"Validation problems found: {len(problems)}"
        )

        for problem in problems:
            print(f"- {problem}")

        raise SystemExit(1)

    print("Validation passed: no problems found.")


if __name__ == "__main__":
    main()

    