from pathlib import Path
from collections import Counter

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

REPORT_OUTPUT = (
    ROOT
    / "reports"
    / "commercial-intelligence-summary.md"
)


EVIDENCE_PRIORITY = {
    "full_scale_deployment": 100,
    "field_deployment": 90,
    "contract": 80,
    "commercial_product": 70,
    "regulatory_or_public_sector_signal": 60,
    "investment": 50,
    "acquisition": 50,
    "partnership": 40,
    "pilot_deployment": 40,
    "scientific_collaboration": 30,
    "other_strategic_signal": 20,
}


MATURITY_PRIORITY = {
    "commercial_full_scale": 100,
    "operational_full_scale": 100,
    "commercial_field_deployment": 90,
    "commercial_public_sector_deployment": 90,
    "government_demonstration": 80,
    "customer_demonstration": 70,
    "third_party_validation": 65,
    "commercial_scale_up": 60,
    "commercial_launch": 55,
    "commercialization_preparation": 50,
    "scale_up": 45,
    "technology_development": 30,
    "corporate_acquisition": 20,
}


COMMERCIALIZATION_MODELS = {
    "originator_and_developer":
        "Technology originator with dedicated commercialization vehicle",

    "developer_and_integrator":
        "Integrated technology developer and commercial vendor",

    "developer_partner_and_integrator":
        "Engineering, integration and technology-development partner",

    "technology_supplier_and_integrator":
        "Technology supplier and integrator within larger corporate platform",
}


def prettify(value):
    if pd.isna(value):
        return ""

    return (
        str(value)
        .replace("_", " ")
        .replace(";", ", ")
    )


def split_multivalue(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def strongest_value(group, column, priorities):
    values = [
        value
        for value in group[column].dropna().unique()
        if str(value).strip()
    ]

    if not values:
        return ""

    return max(
        values,
        key=lambda value: priorities.get(value, 0),
    )


def count_multivalue(series):
    counter = Counter()

    for value in series.dropna():
        counter.update(split_multivalue(value))

    return counter

def count_multivalue_organization_coverage(signals, column):
    coverage = {}

    for _, row in signals.iterrows():
        organization_id = row["organization_id"]

        for value in split_multivalue(row[column]):
            coverage.setdefault(value, set())
            coverage[value].add(organization_id)

    return {
        value: len(organizations)
        for value, organizations in coverage.items()
    }

def markdown_count_table(counter, first_column):
    lines = [
        f"| {first_column} | Signals |",
        "|---|---:|",
    ]

    for value, count in counter.most_common():
        lines.append(
            f"| {prettify(value)} | {count} |"
        )

    return "\n".join(lines)

def markdown_signal_coverage_table(
    signal_counts,
    organization_coverage,
    first_column,
):
    lines = [
        f"| {first_column} | Signals | Organizations |",
        "|---|---:|---:|",
    ]

    for value, count in signal_counts.most_common():
        organizations = organization_coverage.get(
            value,
            0,
        )

        lines.append(
            f"| {prettify(value)} | "
            f"{count} | "
            f"{organizations} |"
        )

    return "\n".join(lines)

def build_organization_summary(organizations, signals):
    rows = []

    for _, organization in organizations.iterrows():
        org_signals = signals.loc[
            signals["organization_id"]
            == organization["organization_id"]
        ]

        strongest_evidence = strongest_value(
            org_signals,
            "evidence_type",
            EVIDENCE_PRIORITY,
        )

        highest_maturity = strongest_value(
            org_signals,
            "maturity_or_deployment_stage",
            MATURITY_PRIORITY,
        )

        rows.append(
            {
                "Organization": organization["normalized_name"],
                "Model": COMMERCIALIZATION_MODELS.get(
                    organization["technology_origin_role"],
                    prettify(
                        organization["technology_origin_role"]
                    ),
                ),
                "Signals": len(org_signals),
                "Strongest evidence": prettify(
                    strongest_evidence
                ),
                "Highest maturity": prettify(
                    highest_maturity
                ),
            }
        )

    return pd.DataFrame(rows)


def dataframe_to_markdown(df):
    headers = list(df.columns)

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(
            ["---"] * len(headers)
        ) + " |",
    ]

    for _, row in df.iterrows():
        values = [
            str(row[column]).replace("|", "\\|")
            for column in headers
        ]

        lines.append(
            "| " + " | ".join(values) + " |"
        )

    return "\n".join(lines)


def main():
    organizations = pd.read_csv(
        ORGANIZATIONS_INPUT
    )

    signals = pd.read_csv(
        SIGNALS_INPUT
    )

    organization_summary = (
        build_organization_summary(
            organizations,
            signals,
        )
    )

    evidence_counts = Counter(
        signals["evidence_type"]
        .dropna()
        .tolist()
    )

    maturity_counts = Counter(
        signals[
            "maturity_or_deployment_stage"
        ]
        .dropna()
        .tolist()
    )

    technology_counts = count_multivalue(
        signals["technology_labels"]
    )

    technology_organization_coverage = (
        count_multivalue_organization_coverage(
            signals,
            "technology_labels",
        )
    )

    treatment_role_counts = Counter(
        signals["treatment_role"]
        .dropna()
        .tolist()
    )

    treatment_role_organization_coverage = (
        signals.groupby("treatment_role")[
            "organization_id"
        ]
        .nunique()
        .to_dict()
    )

    report = [
        "# PFAS Commercial Intelligence — Initial Cross-Company Analysis",
        "",
        "## Scope",
        "",
        (
            f"The current commercial-intelligence pilot contains "
            f"{len(organizations)} organizations and "
            f"{len(signals)} structured strategic signals."
        ),
        "",
        (
            "The objective of this analysis is to identify recurring "
            "commercialization and deployment patterns rather than to "
            "produce a quantitative ranking of companies."
        ),
        "",
        "## Organization comparison",
        "",
        dataframe_to_markdown(
            organization_summary
        ),
        "",
        "## Evidence-type distribution",
        "",
        markdown_count_table(
            evidence_counts,
            "Evidence type",
        ),
        "",
        "## Deployment and maturity signals",
        "",
        markdown_count_table(
            maturity_counts,
            "Maturity / deployment stage",
        ),
        "",
        "## Technology signals",
        "",
        markdown_signal_coverage_table(
            technology_counts,
            technology_organization_coverage,
            "Technology",
        ),
                "## Signal volume versus organization coverage",
        "",
        (
            "Raw signal counts should not be interpreted as direct measures "
            "of market importance or technology leadership."
        ),
        "",
        (
            "A high signal count may reflect deeper research coverage of one "
            "organization rather than broad activity across the market."
        ),
        "",
        (
            "For example, supercritical water oxidation currently has seven "
            "signals but these are associated with a single organization. "
            "By contrast, integrated capture and destroy appears across three "
            "organizations, suggesting a more distributed commercial pattern "
            "despite having fewer total signals."
        ),
        "",
        (
            "For this reason, the commercial-intelligence layer reports both "
            "signal volume and organization coverage. Signal volume indicates "
            "the amount of observed evidence, while organization coverage "
            "indicates how widely that pattern is represented across the "
            "current organization set."
        ),
        "",
        (
            "Neither metric should be used independently as a proxy for "
            "market share, competitive strength or technology leadership."
        ),
        "",
        "",
        "## Treatment roles",
        "",
        markdown_signal_coverage_table(
            treatment_role_counts,
            treatment_role_organization_coverage,
            "Treatment role",
        ),
        "",
        "## Initial strategic findings",
        "",
        "### 1. Multiple commercialization models are visible",
        "",
        (
            "The four organizations represent distinct pathways from "
            "technology development to deployment."
        ),
        "",
        (
            "Battelle combines technology development with a dedicated "
            "commercialization vehicle through Revive Environmental."
        ),
        "",
        (
            "Gradiant combines technology development, integration and "
            "commercial deployment within a single commercial platform."
        ),
        "",
        (
            "Arcadis represents an engineering-led model in which "
            "technology integration, project deployment and research "
            "partnerships coexist."
        ),
        "",
        (
            "Evoqua / Xylem represents an established treatment-technology "
            "supplier whose PFAS capability continues within a larger "
            "corporate platform following acquisition."
        ),
        "",
        "### 2. Commercial evidence extends beyond technology announcements",
        "",
        (
            "The pilot contains full-scale deployments, field deployments, "
            "public-sector contracts, customer demonstrations, corporate "
            "investment and acquisition signals."
        ),
        "",
        (
            "This indicates that the selected organizations are not being "
            "identified solely because of scientific publications or "
            "promotional technology claims."
        ),
        "",
        "### 3. Capture and destruction occupy complementary commercial roles",
        "",
        (
            "Activated carbon and ion exchange appear primarily in mature "
            "capture applications, while supercritical water oxidation and "
            "electrochemical oxidation appear in destruction-oriented or "
            "integrated treatment systems."
        ),
        "",
        (
            "Commercial activity therefore supports the broader technology "
            "landscape finding that capture and destruction are increasingly "
            "being combined rather than treated as mutually exclusive "
            "technology pathways."
        ),
        "",
        "### 4. Integrated treatment is becoming commercially visible",
        "",
        (
            "Battelle / Revive and Gradiant provide particularly clear "
            "examples of systems in which PFAS concentration or media "
            "management is connected with downstream destruction."
        ),
        "",
        (
            "This provides commercial evidence for the broader "
            "capture → concentrate → destroy architecture identified in "
            "the scientific and patent analyses."
        ),
        "",
        "### 5. Corporate structure matters when tracking technology capability",
        "",
        (
            "The Battelle–Revive and Evoqua–Xylem cases show that technology "
            "intelligence cannot rely only on current organization names."
        ),
        "",
        (
            "Capabilities may move through spin-outs, commercialization "
            "vehicles, acquisitions or corporate integration. Maintaining "
            "organization relationships is therefore important for future "
            "monitoring."
        ),
        "",
        "## Interpretation limits",
        "",
        (
            "The current dataset is a deliberately small pilot and does not "
            "represent the complete PFAS treatment market."
        ),
        "",
        (
            "Organizations were selected because they had already generated "
            "strong signals in the scientific, patent or technology-maturity "
            "analysis, which introduces selection bias."
        ),
        "",
        (
            "Signal counts should therefore not be interpreted as measures "
            "of company size, revenue, market share or commercial leadership."
        ),
        "",
        (
            "The purpose of the pilot is to validate the commercial-"
            "intelligence data model and identify evidence patterns that can "
            "support a larger competitive-intelligence workflow."
        ),
        "",
    ]

    REPORT_OUTPUT.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print(
        f"Organizations analysed: "
        f"{len(organizations)}"
    )

    print(
        f"Commercial signals analysed: "
        f"{len(signals)}"
    )

    print(
        f"Report written to: "
        f"{REPORT_OUTPUT}"
    )

    print()
    print("Evidence types:")
    print(evidence_counts)

    print()
    print("Treatment roles:")
    print(treatment_role_counts)

    print()
    print("Technology signals:")
    print(technology_counts)


if __name__ == "__main__":
    main()

