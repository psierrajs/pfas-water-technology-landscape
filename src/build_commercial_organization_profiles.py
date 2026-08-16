from pathlib import Path
import re

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

OUTPUT_DIR = ROOT / "reports" / "organizations"


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def prettify(value):
    if pd.isna(value):
        return ""

    return str(value).replace("_", " ").replace(";", ", ")

def split_semicolon(value):
    if pd.isna(value) or not str(value).strip():
        return []

    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def format_list(values):
    if not values:
        return "- None recorded"

    return "\n".join(
        f"- {prettify(value)}"
        for value in values
    )


def build_signal_section(signals):
    if signals.empty:
        return "No commercial signals recorded."

    sections = []

    signals = signals.sort_values(
        "evidence_date",
        na_position="last",
    )

    for _, signal in signals.iterrows():
        date = signal["evidence_date"]

        if pd.isna(date):
            date = "Date not specified"

        section = [
            f"### {signal['signal_id']} — {prettify(signal['evidence_type'])}",
            "",
            f"**Date:** {date}",
            "",
            f"**Technology:** {prettify(signal['technology_labels'])}",
            "",
            f"**Treatment role:** {prettify(signal['treatment_role'])}",
            "",
            (
                "**Deployment / maturity:** "
                f"{prettify(signal['maturity_or_deployment_stage'])}"
            ),
            "",
        ]

        if pd.notna(signal["partner_organizations"]):
            section.extend(
                [
                    (
				    "**Related organizations:** "
				    f"{str(signal['partner_organizations']).replace(';', ', ')}"
				),
                    "",
                ]
            )

        if pd.notna(signal["location"]):
            section.extend(
                [
                    f"**Location:** {signal['location']}",
                    "",
                ]
            )

        section.extend(
            [
                signal["evidence_summary"],
                "",
                (
                    f"**Evidence confidence:** "
                    f"{prettify(signal['confidence_level'])}"
                ),
                "",
                f"**Source:** [{signal['source_title']}]({signal['source_url']})",
                "",
            ]
        )

        sections.append("\n".join(section))

    return "\n".join(sections)


def build_profile(organization, signals):
    technologies = split_semicolon(
        organization["technology_labels"]
    )

    value_chain_roles = split_semicolon(
        organization["value_chain_roles"]
    )

    target_matrices = split_semicolon(
        organization["target_matrices"]
    )

    organization_signals = signals.loc[
        signals["organization_id"]
        == organization["organization_id"]
    ]

    profile = [
        f"# {organization['normalized_name']} — PFAS Intelligence Profile",
        "",
        "## Organization overview",
        "",
        f"**Organization:** {organization['organization_name']}",
        "",
        f"**Type:** {prettify(organization['organization_type'])}",
        "",
        f"**Headquarters:** {organization['headquarters_country']}",
        "",
        f"**Geographic scope:** {organization['geographic_scope']}",
        "",
        (
            "**Technology origin role:** "
            f"{prettify(organization['technology_origin_role'])}"
        ),
        "",
        (
            "**Commercialization entity:** "
            f"{organization['commercialization_entity']}"
        ),
        "",
        f"**Website:** {organization['website']}",
        "",
        "## Technology focus",
        "",
        format_list(technologies),
        "",
        "## Value-chain roles",
        "",
        format_list(value_chain_roles),
        "",
        "## Target matrices",
        "",
        format_list(target_matrices),
        "",
        "## Current intelligence summary",
        "",
        (
            f"The current dataset contains "
            f"{len(organization_signals)} structured commercial signals "
            f"for {organization['normalized_name']}."
        ),
        "",
        organization["notes"],
        "",
        "## Evidence timeline",
        "",
        build_signal_section(organization_signals),
        "",
        "## Interpretation note",
        "",
        (
            "This profile is generated from the structured commercial-intelligence "
            "dataset. It should be interpreted as an evidence summary rather than "
            "as a definitive assessment of market leadership."
        ),
        "",
    ]

    return "\n".join(profile)


def main():
    organizations = pd.read_csv(ORGANIZATIONS_INPUT)
    signals = pd.read_csv(SIGNALS_INPUT)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for _, organization in organizations.iterrows():
        filename = (
            slugify(organization["normalized_name"])
            + ".md"
        )

        output_path = OUTPUT_DIR / filename

        profile = build_profile(
            organization,
            signals,
        )

        output_path.write_text(
            profile,
            encoding="utf-8",
        )

        print(f"Written: {output_path}")

    print()
    print(f"Organization profiles written: {len(organizations)}")


if __name__ == "__main__":
    main()