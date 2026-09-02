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
    / "commercial-coverage-gaps.md"
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
                }
            )

    relationships = pd.DataFrame(records)

    coverage = (
        relationships
        .groupby("Technology")
        .agg(
            Organization_count=("Organization", "nunique"),
            Organizations=(
                "Organization",
                lambda x: "; ".join(sorted(set(x))),
            ),
        )
        .reset_index()
        .sort_values(
            ["Organization_count", "Technology"],
            ascending=[True, True],
        )
    )

    low_coverage = coverage.loc[
        coverage["Organization_count"] == 1
    ]

    broader_coverage = coverage.loc[
        coverage["Organization_count"] > 1
    ]

    lines = [
        "# Commercial Intelligence Coverage Gaps",
        "",
        "## Purpose",
        "",
        (
            "This report identifies technologies that currently have "
            "limited organization coverage in the commercial-intelligence "
            "pilot."
        ),
        "",
        (
            "Low coverage should be interpreted as a research gap in the "
            "current dataset, not as evidence that few organizations are "
            "commercially active in that technology."
        ),
        "",
        "## Priority coverage gaps",
        "",
        "| Technology | Current organizations | Organization count |",
        "| --- | --- | ---: |",
    ]

    for _, row in low_coverage.iterrows():
        lines.append(
            "| "
            f"{prettify(row['Technology'])} | "
            f"{row['Organizations']} | "
            f"{row['Organization_count']} |"
        )

    lines.extend(
        [
            "",
            "## Technologies with broader current coverage",
            "",
            "| Technology | Current organizations | Organization count |",
            "| --- | --- | ---: |",
        ]
    )

    for _, row in broader_coverage.iterrows():
        lines.append(
            "| "
            f"{prettify(row['Technology'])} | "
            f"{row['Organizations']} | "
            f"{row['Organization_count']} |"
        )

    lines.extend(
        [
            "",
            "## Research implication",
            "",
            (
                "Future organization discovery should prioritize technologies "
                "with single-organization coverage so that the pilot becomes "
                "less dependent on individual company case studies."
            ),
            "",
            (
                "The objective is not to equalize coverage mechanically, but "
                "to distinguish genuine market concentration from incomplete "
                "research coverage."
            ),
            "",
        ]
    )

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Organizations analysed: {len(organizations)}")
    print(f"Technologies analysed: {len(coverage)}")
    print(f"Single-organization technologies: {len(low_coverage)}")
    print(f"Report written to: {OUTPUT}")


if __name__ == "__main__":
    main()