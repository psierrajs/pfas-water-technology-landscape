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

REPORT_OUTPUT = (
    ROOT
    / "reports"
    / "commercial-organization-comparison.md"
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
    "originator_and_developer": (
        "Technology originator with dedicated commercialization vehicle"
    ),
    "developer_and_integrator": (
        "Integrated technology developer and commercial vendor"
    ),
    "developer_partner_and_integrator": (
        "Engineering, integration and technology-development partner"
    ),
    "technology_supplier_and_integrator": (
        "Technology supplier and integrator within larger corporate platform"
    ),
}


def prettify(value):
    if pd.isna(value):
        return ""

    return str(value).replace("_", " ")


def strongest_value(group, column, priority):
    values = [
        value
        for value in group[column].dropna().unique()
        if value
    ]

    if not values:
        return ""

    return max(
        values,
        key=lambda value: priority.get(value, 0),
    )


def collect_partners(group):
    partners = set()

    for value in group["partner_organizations"].dropna():
        for partner in str(value).split(";"):
            partner = partner.strip()

            if partner:
                partners.add(partner)

    return "; ".join(sorted(partners))


def build_comparison(organizations, signals):
    rows = []

    for _, organization in organizations.iterrows():
        organization_id = organization["organization_id"]

        organization_signals = signals.loc[
            signals["organization_id"] == organization_id
        ]

        strongest_evidence = strongest_value(
            organization_signals,
            "evidence_type",
            EVIDENCE_PRIORITY,
        )

        highest_maturity = strongest_value(
            organization_signals,
            "maturity_or_deployment_stage",
            MATURITY_PRIORITY,
        )

        commercialization_model = COMMERCIALIZATION_MODELS.get(
            organization["technology_origin_role"],
            prettify(organization["technology_origin_role"]),
        )

        rows.append(
            {
                "Organization": organization["normalized_name"],
                "Organization type": prettify(
                    organization["organization_type"]
                ),
                "Technology focus": str(
                    organization["technology_labels"]
                ).replace("_", " ").replace(";", ", "),
                "Commercialization model": commercialization_model,
                "Strongest evidence": prettify(strongest_evidence),
                "Highest maturity": prettify(highest_maturity),
                "Signals": len(organization_signals),
                "Related organizations": collect_partners(organization_signals),
            }
        )

    return pd.DataFrame(rows)


def dataframe_to_markdown(df):
    headers = list(df.columns)

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for _, row in df.iterrows():
        values = [
            str(row[column]).replace("|", "\\|")
            for column in headers
        ]

        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def write_report(comparison):
    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# Commercial Organization Comparison",
        "",
        "## Purpose",
        "",
        (
            "This report compares the organizations included in the initial "
            "PFAS commercial-intelligence pilot."
        ),
        "",
        (
            "The comparison is derived from the structured organization and "
            "commercial-signal datasets rather than from a manually assigned "
            "overall ranking."
        ),
        "",
        "## Organization comparison",
        "",
        dataframe_to_markdown(comparison),
        "",
        "## Interpretation",
        "",
        (
            "The current pilot contains organizations with substantially "
            "different commercialization models."
        ),
        "",
        (
            "- Battelle represents a technology-originator model in which "
            "commercial deployment is scaled through a dedicated commercialization "
            "vehicle."
        ),
        (
            "- Gradiant represents an integrated technology-vendor model combining "
            "PFAS concentration and destructive treatment within a commercial "
            "platform."
        ),
        (
            "- Arcadis represents an engineering and integration model combining "
            "commercial deployment with technology-development partnerships."
        ),
        (
            "- Evoqua / Xylem represents an established treatment-technology "
            "supplier whose PFAS capabilities continue within a larger corporate "
            "platform following acquisition."
        ),
        "",
        (
            "The comparison is intended as an initial intelligence framework. "
            "Evidence coverage is not yet sufficiently broad or standardized to "
            "support a quantitative ranking of organizations."
        ),
        "",
    ]

    REPORT_OUTPUT.write_text(
        "\n".join(report),
        encoding="utf-8",
    )


def main():
    organizations = pd.read_csv(ORGANIZATIONS_INPUT)
    signals = pd.read_csv(SIGNALS_INPUT)

    comparison = build_comparison(
        organizations,
        signals,
    )

    write_report(comparison)

    print(f"Organizations compared: {len(comparison)}")
    print(f"Commercial signals used: {len(signals)}")
    print(f"Report written to: {REPORT_OUTPUT}")

    print()
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()