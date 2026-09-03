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

OUTPUT = (
    ROOT
    / "reports"
    / "commercial-research-priorities.md"
)


def prettify(value):
    return str(value).replace("_", " ")


def split_multivalue(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def main():
    organizations = pd.read_csv(ORGANIZATIONS_INPUT)
    signals = pd.read_csv(SIGNALS_INPUT)

    organization_records = []

    for _, organization in organizations.iterrows():
        for technology in split_multivalue(
            organization["technology_labels"]
        ):
            organization_records.append(
                {
                    "Technology": technology,
                    "Organization": organization["normalized_name"],
                }
            )

    organization_relationships = pd.DataFrame(
        organization_records
    )

    organization_coverage = (
        organization_relationships
        .groupby("Technology")["Organization"]
        .nunique()
        .to_dict()
    )

    signal_records = []

    for _, signal in signals.iterrows():
        for technology in split_multivalue(
            signal["technology_labels"]
        ):
            signal_records.append(
                {
                    "Technology": technology,
                    "Signal": signal["signal_id"],
                }
            )

    signal_relationships = pd.DataFrame(
        signal_records
    )

    signal_counts = (
        signal_relationships
        .groupby("Technology")["Signal"]
        .nunique()
        .to_dict()
    )

    technologies = sorted(
        set(organization_coverage)
        | set(signal_counts)
    )

    rows = []

    for technology in technologies:
        org_count = organization_coverage.get(
            technology,
            0,
        )

        signal_count = signal_counts.get(
            technology,
            0,
        )

        if org_count == 1:
            priority = "High"
            rationale = (
                "Single-organization coverage; additional organization "
                "discovery would help distinguish market concentration "
                "from incomplete research coverage."
            )
        elif org_count == 2:
            priority = "Medium"
            rationale = (
                "Some cross-organization coverage exists, but additional "
                "commercial evidence would improve comparative confidence."
            )
        else:
            priority = "Lower"
            rationale = (
                "Broader organization coverage already exists in the "
                "current pilot."
            )

        rows.append(
            {
                "Technology": technology,
                "Organization count": org_count,
                "Signal count": signal_count,
                "Research priority": priority,
                "Rationale": rationale,
            }
        )

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Lower": 2,
    }

    rows = sorted(
        rows,
        key=lambda row: (
            priority_order[row["Research priority"]],
            row["Organization count"],
            -row["Signal count"],
            row["Technology"],
        ),
    )

    lines = [
        "# Commercial Intelligence Research Priorities",
        "",
        "## Purpose",
        "",
        (
            "This report converts current organization coverage and "
            "commercial-signal volume into a practical research-priority "
            "view for the next phase of the PFAS commercial-intelligence "
            "pilot."
        ),
        "",
        (
            "Priority reflects gaps in the current dataset rather than "
            "an assessment of technology quality or market attractiveness."
        ),
        "",
        "## Research priorities",
        "",
        (
            "| Technology | Organization count | Signal count | "
            "Research priority | Rationale |"
        ),
        "| --- | ---: | ---: | --- | --- |",
    ]

    for row in rows:
        lines.append(
            "| "
            f"{prettify(row['Technology'])} | "
            f"{row['Organization count']} | "
            f"{row['Signal count']} | "
            f"{row['Research priority']} | "
            f"{row['Rationale']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "High-priority technologies should be investigated first "
                "when expanding the organization set because they currently "
                "depend on evidence from a single commercial organization."
            ),
            "",
            (
                "Signal volume is retained alongside organization coverage "
                "so that a technology with many signals from one organization "
                "can be distinguished from a technology represented across "
                "several organizations."
            ),
            "",
            (
                "These priorities are intended to guide evidence collection, "
                "not to rank technologies by commercial potential."
            ),
            "",
        ]
    )

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Organizations analysed: {len(organizations)}")
    print(f"Commercial signals analysed: {len(signals)}")
    print(f"Technologies prioritised: {len(rows)}")
    print(f"Report written to: {OUTPUT}")


if __name__ == "__main__":
    main()