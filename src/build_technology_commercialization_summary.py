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

OUTPUT = (
    ROOT
    / "reports"
    / "technology-commercialization-summary.md"
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

    records = []

    for _, organization in organizations.iterrows():
        for technology in split_multivalue(
            organization["technology_labels"]
        ):
            records.append(
                {
                    "Technology": technology,
                    "Organization": organization["normalized_name"],
                    "Origin role": organization["technology_origin_role"],
                    "Commercialization entity": (
                        organization["commercialization_entity"]
                    ),
                }
            )

    relationships = pd.DataFrame(records)

    grouped = (
        relationships
        .groupby("Technology")
        .agg(
            Organizations=("Organization", lambda x: "; ".join(sorted(set(x)))),
            Organization_count=("Organization", "nunique"),
            Origin_roles=("Origin role", lambda x: "; ".join(sorted(set(x)))),
            Commercialization_entities=(
                "Commercialization entity",
                lambda x: "; ".join(sorted(set(x))),
            ),
        )
        .reset_index()
        .sort_values(
            ["Organization_count", "Technology"],
            ascending=[False, True],
        )
    )

    lines = [
        "# Technology Commercialization Summary",
        "",
        "## Purpose",
        "",
        (
            "This report provides a technology-centric view of the current "
            "PFAS commercial-intelligence pilot."
        ),
        "",
        (
            "It complements the organization-centric network by showing "
            "which treatment technologies are represented across multiple "
            "organizations and commercialization models."
        ),
        "",
        "## Technology coverage",
        "",
        (
            "| Technology | Organizations | Organization count | "
            "Origin roles | Commercialization entities |"
        ),
        "| --- | --- | ---: | --- | --- |",
    ]

    for _, row in grouped.iterrows():
        lines.append(
            "| "
            f"{prettify(row['Technology'])} | "
            f"{row['Organizations']} | "
            f"{row['Organization_count']} | "
            f"{prettify(row['Origin_roles'])} | "
            f"{row['Commercialization_entities']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "Technologies represented by multiple organizations provide "
                "stronger evidence of broader commercial activity than "
                "technologies currently associated with a single organization "
                "in the pilot."
            ),
            "",
            (
                "Single-organization coverage should not be interpreted as "
                "evidence that a technology lacks wider market activity. It "
                "may instead reflect the deliberately limited scope of the "
                "current commercial-intelligence dataset."
            ),
            "",
            (
                "Future iterations can combine this view with deployment "
                "maturity, signal volume and organization coverage to identify "
                "technologies with both broad participation and strong "
                "commercial evidence."
            ),
            "",
        ]
    )

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Organizations analysed: {len(organizations)}")
    print(f"Technologies summarised: {len(grouped)}")
    print(f"Relationships analysed: {len(relationships)}")
    print(f"Report written to: {OUTPUT}")


if __name__ == "__main__":
    main()