from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

ORGANIZATIONS_OUTPUT = (
    ROOT / "data" / "processed" / "commercial_intelligence" / "organizations.csv"
)

SIGNALS_OUTPUT = (
    ROOT / "data" / "processed" / "commercial_intelligence" / "commercial-signals.csv"
)

ORGANIZATION_FIELDS = [
    "organization_id",
    "organization_name",
    "normalized_name",
    "organization_type",
    "headquarters_country",
    "geographic_scope",
    "technology_labels",
    "value_chain_roles",
    "technology_origin_role",
    "commercialization_entity",
    "target_matrices",
    "website",
    "notes",
]

SIGNAL_FIELDS = [
    "signal_id",
    "organization_id",
    "organization_name",
    "evidence_date",
    "evidence_type",
    "technology_labels",
    "treatment_role",
    "target_matrix",
    "maturity_or_deployment_stage",
    "partner_organizations",
    "location",
    "source_title",
    "source_url",
    "source_type",
    "evidence_summary",
    "confidence_level",
    "verification_status",
    "date_accessed",
    "notes",
]


organizations = [
    {
        "organization_id": "ORG-001",
        "organization_name": "Battelle Memorial Institute",
        "normalized_name": "Battelle",
        "organization_type": "research_and_technology_organization",
        "headquarters_country": "United States",
        "geographic_scope": "United States; global",
        "technology_labels": (
            "supercritical_water_oxidation;"
            "activated_carbon_regeneration;"
            "integrated_capture_and_destroy"
        ),
        "value_chain_roles": (
            "technology_development;"
            "technology_validation;"
            "technology_commercialization"
        ),
        "technology_origin_role": "originator_and_developer",
        "commercialization_entity": "Revive Environmental",
        "target_matrices": (
            "landfill_leachate;"
            "industrial_wastewater;"
            "groundwater;"
            "AFFF;"
            "PFAS_concentrates"
        ),
        "website": "https://www.battelle.org/",
        "notes": (
            "Developer of PFAS ANNIHILATOR and GAC Renew. "
            "Commercial deployment transferred/scaled through Revive Environmental."
        ),
    }
]


signals = [
    {
        "signal_id": "SIG-0001",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2022-03-29",
        "evidence_type": "partnership",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "wastewater;landfill_leachate",
        "maturity_or_deployment_stage": "commercialization_preparation",
        "partner_organizations": "Heritage-Crystal Clean",
        "location": "United States",
        "source_title": (
            "Heritage-Crystal Clean, Inc. and Battelle to Collaborate "
            "on PFAS Destruction for Wastewater"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "heritage-crystal-clean-inc.-and-battelle-to-collaborate-on-pfas-"
            "destruction-for-wastewater"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Battelle selected Heritage-Crystal Clean as a partner to use, market "
            "and service the PFAS ANNIHILATOR for commercial applications, including "
            "wastewater treatment plants and third-party sites."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0002",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2022-04-27",
        "evidence_type": "pilot_deployment",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "landfill_leachate",
        "maturity_or_deployment_stage": "customer_demonstration",
        "partner_organizations": "Heritage-Crystal Clean",
        "location": "Michigan, United States",
        "source_title": (
            "Battelle PFAS ANNIHILATOR Mobile Unit Makes First-Ever "
            "Customer Engagement to Destroy Forever Chemicals"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "battelle-pfas-annihilatortm-mobile-unit-makes-first-ever-commercial-"
            "demonstration-to-destroy-forever-chemicals"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Battelle deployed a mobile PFAS ANNIHILATOR unit for a weeklong "
            "customer engagement at a Heritage-Crystal Clean wastewater treatment "
            "facility in western Michigan."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0003",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2022-06-20",
        "evidence_type": "other_strategic_signal",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "AFFF;landfill_leachate;industrial_wastewater",
        "maturity_or_deployment_stage": "scale_up",
        "partner_organizations": "Heritage-Crystal Clean",
        "location": "United States",
        "source_title": (
            "Battelle's Proven Technology Ready to Address PFAS Threats "
            "to Drinking Water"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "battelle-s-proven-technology-ready-to-address-pfas-threats-to-"
            "drinking-water"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Battelle reported fabrication of a fixed-base PFAS ANNIHILATOR unit "
            "following the Michigan deployment and described planned treatment "
            "activity involving AFFF and other aqueous PFAS wastes."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0004",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2023-01-17",
        "evidence_type": "investment",
        "technology_labels": (
            "supercritical_water_oxidation;"
            "activated_carbon_regeneration;"
            "integrated_capture_and_destroy"
        ),
        "treatment_role": "integrated_treatment",
        "target_matrix": (
            "landfill_leachate;"
            "municipal_wastewater;"
            "groundwater;"
            "AFFF"
        ),
        "maturity_or_deployment_stage": "commercial_scale_up",
        "partner_organizations": "Viking Global Investors;Revive Environmental",
        "location": "Columbus, Ohio, United States",
        "source_title": (
            "Battelle, Viking Global Investors Launch Revive Environmental"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "battelle-viking-global-investors-launch-revive-environmental"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Battelle and Viking Global Investors launched Revive Environmental "
            "to scale PFAS ANNIHILATOR and GAC Renew for commercial contaminant "
            "mitigation and PFAS treatment."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": (
            "This signal is classified as investment because Viking contributed "
            "capital to the jointly owned commercialization vehicle."
        ),
    },
    {
        "signal_id": "SIG-0005",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2023-05-01",
        "evidence_type": "full_scale_deployment",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "landfill_leachate_concentrate",
        "maturity_or_deployment_stage": "commercial_full_scale",
        "partner_organizations": "Revive Environmental;Heritage-Crystal Clean",
        "location": "Grand Rapids, Michigan, United States",
        "source_title": (
            "Revive Environmental PFAS ANNIHILATOR Deployed in First-to-Market "
            "Commercial Destruction of Forever Chemicals"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "revive-environmental-pfas-annihilator-deployed-in-first-to-market-"
            "commercial-destruction-of-forever-chemicals"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Revive deployed the full-scale PFAS ANNIHILATOR at a "
            "Heritage-Crystal Clean facility in Grand Rapids to treat concentrated "
            "PFAS waste generated from more than 160,000 gallons of landfill "
            "leachate per day."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0006",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2023-07-18",
        "evidence_type": "contract",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "AFFF",
        "maturity_or_deployment_stage": "commercial_public_sector_deployment",
        "partner_organizations": "Revive Environmental;State of New Hampshire",
        "location": "New Hampshire, United States",
        "source_title": (
            "State of New Hampshire Chooses Revive Environmental's "
            "PFAS ANNIHILATOR System to Destroy Harmful Firefighting Foam Stockpiles"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "state-of-new-hampshire-chooses-revive-environmental-s-pfas-"
            "annihilatortm-system-to-destroy-harmful-firefighting-foam-stockpiles"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "The State of New Hampshire selected Revive Environmental's PFAS "
            "ANNIHILATOR system for destruction of PFAS-containing firefighting "
            "foam stockpiles."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0007",
        "organization_id": "ORG-001",
        "organization_name": "Battelle",
        "evidence_date": "2023-12-12",
        "evidence_type": "regulatory_or_public_sector_signal",
        "technology_labels": "supercritical_water_oxidation",
        "treatment_role": "destruction",
        "target_matrix": "PFAS_contaminated_waste",
        "maturity_or_deployment_stage": "government_demonstration",
        "partner_organizations": (
            "Revive Environmental;United States Department of Defense"
        ),
        "location": "United States",
        "source_title": (
            "Battelle, Revive Environmental to Demonstrate PFAS Technology "
            "in Department of Defense Project"
        ),
        "source_url": (
            "https://www.battelle.org/insights/newsroom/press-release-details/"
            "battelle--revive-environmental-to-demonstrate-pfas-technology-in-"
            "department-of-defense-project"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Battelle and Revive Environmental announced a U.S. Department of "
            "Defense demonstration project involving PFAS destruction technology."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
]


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    write_csv(
        ORGANIZATIONS_OUTPUT,
        ORGANIZATION_FIELDS,
        organizations,
    )

    write_csv(
        SIGNALS_OUTPUT,
        SIGNAL_FIELDS,
        signals,
    )

    print(f"Organizations written: {len(organizations)}")
    print(f"Commercial signals written: {len(signals)}")
    print(f"Organizations output: {ORGANIZATIONS_OUTPUT}")
    print(f"Signals output: {SIGNALS_OUTPUT}")


if __name__ == "__main__":
    main()