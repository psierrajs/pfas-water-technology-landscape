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
    / "organization-technology-network.md"
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

    rows = []

    for _, organization in organizations.iterrows():
        for technology in split_multivalue(
            organization["technology_labels"]
        ):
            rows.append(
                {
                    "Organization": organization["normalized_name"],
                    "Technology": prettify(technology),
                    "Origin role": prettify(
                        organization["technology_origin_role"]
                    ),
                    "Commercialization entity": (
                        organization["commercialization_entity"]
                    ),
                }
            )

    network = pd.DataFrame(rows).sort_values(
        ["Technology", "Organization"]
    )

    lines = [
        "# Organization–Technology Network",
        "",
        "## Purpose",
        "",
        (
            "This report provides a lightweight organization–technology "
            "relationship view for the PFAS commercial-intelligence pilot."
        ),
        "",
        (
            "It is intended as a first step toward a richer intelligence "
            "network linking organizations, technologies, commercialization "
            "entities and strategic signals."
        ),
        "",
        "## Organization–technology relationships",
        "",
        "| Organization | Technology | Origin role | Commercialization entity |",
        "| --- | --- | --- | --- |",
    ]

    for _, row in network.iterrows():
        lines.append(
            "| "
            f"{row['Organization']} | "
            f"{row['Technology']} | "
            f"{row['Origin role']} | "
            f"{row['Commercialization entity']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "The current pilot already shows that individual PFAS "
                "technologies can appear across different commercialization "
                "models, while individual organizations may span multiple "
                "technology categories."
            ),
            "",
            (
                "Future extensions can add research institutions, ownership "
                "relationships, licensing links, partnerships and deployment "
                "signals to form a more complete competitive-intelligence "
                "network."
            ),
            "",
        ]
    )

    OUTPUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Organizations analysed: {len(organizations)}")
    print(f"Relationships written: {len(network)}")
    print(f"Report written to: {OUTPUT}")


if __name__ == "__main__":
    main()