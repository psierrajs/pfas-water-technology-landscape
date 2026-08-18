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
    },
        {
        "organization_id": "ORG-002",
        "organization_name": "Gradiant",
        "normalized_name": "Gradiant",
        "organization_type": "water_technology_company",
        "headquarters_country": "United States",
        "geographic_scope": "global",
        "technology_labels": (
            "foam_fractionation;"
            "electrochemical_oxidation;"
            "integrated_capture_and_destroy"
        ),
        "value_chain_roles": (
            "technology_development;"
            "system_integration;"
            "commercial_deployment"
        ),
        "technology_origin_role": "developer_and_integrator",
        "commercialization_entity": "Gradiant",
        "target_matrices": (
            "industrial_wastewater;"
            "municipal_water;"
            "landfill_leachate;"
            "RO_concentrate;"
            "AFFF_contaminated_groundwater"
        ),
        "website": "https://www.gradiant.com/",
        "notes": (
            "Developer and commercial supplier of ForeverGone, integrating "
            "micro-foam fractionation with electro-oxidation for PFAS "
            "concentration and destruction."
        ),
    },
        {
        "organization_id": "ORG-003",
        "organization_name": "Arcadis",
        "normalized_name": "Arcadis",
        "organization_type": "engineering_and_environmental_services_company",
        "headquarters_country": "Netherlands",
        "geographic_scope": "global",
        "technology_labels": (
            "activated_carbon;"
            "ion_exchange;"
            "foam_fractionation;"
            "sonolysis;"
            "integrated_treatment"
        ),
        "value_chain_roles": (
            "engineering;"
            "technology_integration;"
            "commercial_deployment;"
            "technology_development"
        ),
        "technology_origin_role": "developer_partner_and_integrator",
        "commercialization_entity": "Arcadis",
        "target_matrices": (
            "groundwater;"
            "surface_water;"
            "landfill_leachate;"
            "industrial_wastewater;"
            "AFFF_contaminated_water"
        ),
        "website": "https://www.arcadis.com/",
        "notes": (
            "Global engineering and environmental-services company with PFAS "
            "deployment experience and development partnerships in fractionation "
            "and destructive treatment technologies."
        ),
    },
        {
        "organization_id": "ORG-004",
        "organization_name": "Evoqua Water Technologies / Xylem",
        "normalized_name": "Evoqua / Xylem",
        "organization_type": "water_technology_company",
        "headquarters_country": "United States",
        "geographic_scope": "global",
        "technology_labels": (
            "ion_exchange;"
            "activated_carbon;"
            "adsorption;"
            "integrated_treatment"
        ),
        "value_chain_roles": (
            "technology_supply;"
            "system_integration;"
            "commercial_deployment;"
            "service"
        ),
        "technology_origin_role": "technology_supplier_and_integrator",
        "commercialization_entity": "Xylem",
        "target_matrices": (
            "drinking_water;"
            "groundwater;"
            "municipal_water;"
            "industrial_water"
        ),
        "website": "https://www.xylem.com/",
        "notes": (
            "Evoqua developed and deployed PFAS treatment systems using ion "
            "exchange and other adsorption media. Xylem completed its acquisition "
            "of Evoqua in 2023 and continues to surface Evoqua PFAS capabilities."
        ),
    },
        {
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "normalized_name": "Aquagga",
        "organization_type": "water_technology_startup",
        "headquarters_country": "United States",
        "geographic_scope": "United States; global",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction;"
            "integrated_capture_and_destroy"
        ),
        "value_chain_roles": (
            "technology_development;"
            "technology_commercialization;"
            "commercial_deployment;"
            "system_integration"
        ),
        "technology_origin_role": "licensed_technology_developer",
        "commercialization_entity": "Aquagga",
        "target_matrices": (
            "industrial_wastewater;"
            "PFAS_concentrates;"
            "AFFF;"
            "landfill_leachate;"
            "high_TDS_wastewater"
        ),
        "website": "https://www.aquagga.com/",
        "notes": (
            "Commercial developer of Hydrothermal Alkaline Treatment (HALT) "
            "for PFAS destruction. Aquagga holds exclusive licenses to "
            "foundational HALT and hydrothermal-processing intellectual "
            "property and is progressing the technology through commercial "
            "systems and field demonstrations."
        ),
    },
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
        {
        "signal_id": "SIG-0008",
        "organization_id": "ORG-002",
        "organization_name": "Gradiant",
        "evidence_date": "2024-05-15",
        "evidence_type": "commercial_product",
        "technology_labels": (
            "foam_fractionation;"
            "electrochemical_oxidation;"
            "integrated_capture_and_destroy"
        ),
        "treatment_role": "integrated_treatment",
        "target_matrix": "municipal_water;industrial_wastewater",
        "maturity_or_deployment_stage": "commercial_launch",
        "partner_organizations": "",
        "location": "United States; global",
        "source_title": (
            "Gradiant Launches ForeverGone, the Industry's Only Complete "
            "PFAS Removal and Destruction Solution"
        ),
        "source_url": (
            "https://www.gradiant.com/press-release/"
            "gradiant-launches-forevergone-the-industrys-only-complete-"
            "pfas-removal-and-destruction-solution/"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Gradiant commercially launched ForeverGone, integrating "
            "micro-foam fractionation for PFAS concentration with an "
            "electro-oxidation destruction engine."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
    {
        "signal_id": "SIG-0009",
        "organization_id": "ORG-002",
        "organization_name": "Gradiant",
        "evidence_date": "2024-10-08",
        "evidence_type": "other_strategic_signal",
        "technology_labels": (
            "foam_fractionation;"
            "electrochemical_oxidation;"
            "integrated_capture_and_destroy"
        ),
        "treatment_role": "integrated_treatment",
        "target_matrix": (
            "industrial_wastewater;"
            "municipal_water;"
            "landfill_water"
        ),
        "maturity_or_deployment_stage": "third_party_validation",
        "partner_organizations": "multiple accredited laboratories",
        "location": "United States",
        "source_title": (
            "ForeverGone is Proven to Remove and Completely Destroy PFAS "
            "in Industrial and Municipal Applications"
        ),
        "source_url": (
            "https://www.gradiant.com/press-release/"
            "forevergone-is-proven-to-remove-and-completely-destroy-pfas-"
            "in-industrial-and-municipal-applications/"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Gradiant reported third-party accredited laboratory validation "
            "of ForeverGone using contaminated industrial, municipal and "
            "landfill waters, with removal below regulatory limits and "
            "destruction of the concentrated PFAS stream."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": (
            "Performance claims originate from Gradiant but explicitly reference "
            "multiple third-party accredited laboratories."
        ),
    },
    {
        "signal_id": "SIG-0010",
        "organization_id": "ORG-002",
        "organization_name": "Gradiant",
        "evidence_date": "2025-09-29",
        "evidence_type": "field_deployment",
        "technology_labels": (
            "foam_fractionation;"
            "electrochemical_oxidation;"
            "integrated_capture_and_destroy"
        ),
        "treatment_role": "integrated_treatment",
        "target_matrix": "PFAS_contaminated_water",
        "maturity_or_deployment_stage": "commercial_field_deployment",
        "partner_organizations": "Munich International Airport",
        "location": "Munich, Germany",
        "source_title": (
            "Gradiant's ForeverGone Sets New Standard for PFAS Destruction "
            "with Breakthrough Cost and Performance"
        ),
        "source_url": (
            "https://www.gradiant.com/press-release/"
            "forevergone-pfas-destruction-munich-airport/"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Gradiant reported deployment of the ForeverGone PFAS treatment "
            "platform at Munich International Airport, providing a commercial "
            "field-deployment signal for the integrated concentration-and-"
            "destruction system."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-15",
        "notes": "",
    },
        {
        "signal_id": "SIG-0011",
        "organization_id": "ORG-003",
        "organization_name": "Arcadis",
        "evidence_date": "2021-08-17",
        "evidence_type": "commercial_product",
        "technology_labels": "foam_fractionation",
        "treatment_role": "concentration",
        "target_matrix": "landfill_leachate;industrial_wastewater",
        "maturity_or_deployment_stage": "commercial_launch",
        "partner_organizations": "Evocra",
        "location": "North America",
        "source_title": (
            "Arcadis launches revolutionary mobile PFAS removal technology"
        ),
        "source_url": (
            "https://www.arcadis.com/en-us/news/north-america/united-states/"
            "2021/8/arcadis-launches-revolutionary-mobile-pfas-removal-technology"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Arcadis and Evocra launched a commercially available portable "
            "fractionation system for PFAS-contaminated water following a "
            "two-year pilot collaboration with North American clients."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": (
            "Arcadis reports up to 99% removal of targeted PFAS and major "
            "reduction in contaminated waste-stream volume."
        ),
    },
    {
        "signal_id": "SIG-0012",
        "organization_id": "ORG-003",
        "organization_name": "Arcadis",
        "evidence_date": "",
        "evidence_type": "full_scale_deployment",
        "technology_labels": "activated_carbon",
        "treatment_role": "capture",
        "target_matrix": "groundwater;surface_water",
        "maturity_or_deployment_stage": "operational_full_scale",
        "partner_organizations": "Guernsey Airport",
        "location": "Guernsey, United Kingdom",
        "source_title": (
            "Safeguarding Guernsey’s drinking water from PFAS contamination"
        ),
        "source_url": (
            "https://www.arcadis.com/en/projects/europe/united-kingdom/"
            "protecting-guernseys-water-from-pfass"
        ),
        "source_type": "company_project_case_study",
        "evidence_summary": (
            "Arcadis designed and installed a granular activated carbon treatment "
            "system for PFAS-impacted groundwater and surface water associated "
            "with Guernsey Airport. Arcadis reports treatment capacity of up to "
            "20 litres per second."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": (
            "Source does not provide a clear project publication or commissioning "
            "date, so evidence_date is intentionally left blank."
        ),
    },
    {
        "signal_id": "SIG-0013",
        "organization_id": "ORG-003",
        "organization_name": "Arcadis",
        "evidence_date": "",
        "evidence_type": "scientific_collaboration",
        "technology_labels": "sonolysis;integrated_capture_and_destroy",
        "treatment_role": "destruction",
        "target_matrix": "PFAS_contaminated_water;liquid_waste",
        "maturity_or_deployment_stage": "technology_development",
        "partner_organizations": "University of Surrey",
        "location": "United Kingdom",
        "source_title": "Arcadis Global PFAS Remediation Experts — Our Solutions",
        "source_url": "https://www.arcadis.com/campaigns/pfasau/index.html",
        "source_type": "company_technology_page",
        "evidence_summary": (
            "Arcadis identifies sonolysis as a destructive PFAS technology under "
            "development with an international scientific team, with the stated "
            "goal of developing it into a viable commercial remediation option."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": (
            "University of Surrey research records independently show Arcadis "
            "participation in PFAS sonolysis scale-up research."
        ),
    }, 
        {
        "signal_id": "SIG-0014",
        "organization_id": "ORG-004",
        "organization_name": "Evoqua / Xylem",
        "evidence_date": "2023-01-23",
        "evidence_type": "acquisition",
        "technology_labels": "ion_exchange;activated_carbon",
        "treatment_role": "integrated_treatment",
        "target_matrix": "municipal_water;industrial_water",
        "maturity_or_deployment_stage": "corporate_acquisition",
        "partner_organizations": "Xylem;Evoqua Water Technologies",
        "location": "United States",
        "source_title": (
            "Xylem To Acquire Evoqua in $7.5 Billion All-Stock Transaction"
        ),
        "source_url": (
            "https://www.xylem.com/en-us/about-xylem/newsroom/press-releases/"
            "xylem-to-acquire-evoqua-in-%247.5-billion-all-stock-transaction/"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Xylem announced an agreement to acquire Evoqua for approximately "
            "$7.5 billion. Xylem specifically identified Evoqua as a leader in "
            "remediation of emerging contaminants including PFAS."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": (
            "Useful ownership-continuity signal for tracking PFAS capability "
            "after the Evoqua brand became part of Xylem."
        ),
    },
    {
        "signal_id": "SIG-0015",
        "organization_id": "ORG-004",
        "organization_name": "Evoqua / Xylem",
        "evidence_date": "",
        "evidence_type": "full_scale_deployment",
        "technology_labels": "ion_exchange",
        "treatment_role": "capture",
        "target_matrix": "drinking_water;groundwater",
        "maturity_or_deployment_stage": "operational_full_scale",
        "partner_organizations": "Santa Clarita Valley Water Agency",
        "location": "California, United States",
        "source_title": (
            "SCV Water Agency Selects Evoqua Vessels & Media For PFAS Removal"
        ),
        "source_url": (
            "https://www.xylem.com/en-uk/resources/case-studies/"
            "scv-water-agency-selects-evoqua-vessels--media-for-pfas-removal/"
        ),
        "source_type": "company_case_study",
        "evidence_summary": (
            "Evoqua supplied three lead-lag vessel systems using ion-exchange "
            "resin to remove PFAS from drinking-water wells and return previously "
            "decommissioned wells to service. The combined systems can process "
            "up to 6,000 gallons per minute."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": (
            "Source states that PSR2 Plus was one of the selected ion-exchange "
            "resins. Event date is not explicit on the case-study page."
        ),
    },
    {
        "signal_id": "SIG-0016",
        "organization_id": "ORG-004",
        "organization_name": "Evoqua / Xylem",
        "evidence_date": "2024-02-15",
        "evidence_type": "full_scale_deployment",
        "technology_labels": "ion_exchange",
        "treatment_role": "capture",
        "target_matrix": "drinking_water;groundwater",
        "maturity_or_deployment_stage": "operational_full_scale",
        "partner_organizations": "Stratmoor Hills Water District",
        "location": "Colorado, United States",
        "source_title": (
            "Colorado utility removes PFCs from well with Xylem's "
            "ion exchange system"
        ),
        "source_url": (
            "https://www.xylem.com/en-ie/making-waves/water-utilities-news/"
            "colorado-utility-removes-pfcs-from-well-with-xylems-ion-exchange-system/"
        ),
        "source_type": "company_case_study",
        "evidence_summary": (
            "Evoqua, now a Xylem company, supplied a selective single-use "
            "ion-exchange system for PFAS-contaminated groundwater. The initial "
            "installation led to expansion into a permanent treatment facility "
            "capable of producing up to 1.1 million gallons of treated water "
            "per day."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-16",
        "notes": "",
    },   
        {
        "signal_id": "SIG-0017",
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "evidence_date": "2024-04-01",
        "evidence_type": "field_deployment",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction"
        ),
        "treatment_role": "destruction",
        "target_matrix": "industrial_wastewater",
        "maturity_or_deployment_stage": "commercial_field_deployment",
        "partner_organizations": "3M Company",
        "location": "United States",
        "source_title": (
            "Case Study - Real World Industrial PFAS Destruction"
        ),
        "source_url": (
            "https://www.aquagga.com/"
            "case-study-real-world-industrial-pfas-destruction"
        ),
        "source_type": "company_case_study",
        "evidence_summary": (
            "Aquagga deployed a commercial-scale HALT system at an "
            "industrial manufacturing facility for continuous treatment "
            "of complex PFAS-containing wastewater. The demonstration "
            "treated real industrial wastewater and was presented as a "
            "transition from product development toward commercial deployment."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-18",
        "notes": (
            "Aquagga reports greater than 99% total PFAS destruction "
            "and greater than 95% measured defluorination."
        ),
    },
    {
        "signal_id": "SIG-0018",
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "evidence_date": "",
        "evidence_type": "commercial_product",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction"
        ),
        "treatment_role": "destruction",
        "target_matrix": "PFAS_concentrates",
        "maturity_or_deployment_stage": "commercial_launch",
        "partner_organizations": "",
        "location": "United States; global",
        "source_title": "Hydrothermal Alkaline Treatment PFAS Destruction",
        "source_url": "https://www.aquagga.com/ourtech",
        "source_type": "company_technology_page",
        "evidence_summary": (
            "Aquagga states that its HALT systems are commercially "
            "available to order, with product configurations offered for "
            "lease, purchase or demonstration projects."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-18",
        "notes": (
            "Product families listed include Colt, Steed and Stampede systems."
        ),
    },
    {
        "signal_id": "SIG-0019",
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "evidence_date": "2025-06-02",
        "evidence_type": "regulatory_or_public_sector_signal",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction"
        ),
        "treatment_role": "destruction",
        "target_matrix": "AFFF;PFAS_concentrates",
        "maturity_or_deployment_stage": "government_demonstration",
        "partner_organizations": (
            "United States Department of Defense;"
            "Defense Innovation Unit;"
            "United States Air Force;"
            "United States Navy"
        ),
        "location": "United States",
        "source_title": (
            "Aquagga, Inc. Demonstrates Successful PFAS Destruction "
            "with DoD-Funded Project"
        ),
        "source_url": (
            "https://www.aquagga.com/blog/"
            "aquagga-validates-halt-technology-in-dod-funded-demonstration-project"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Aquagga reported completion of a DoD-funded HALT demonstration "
            "involving concentrated PFAS-containing liquids and an AFFF "
            "mixture, providing public-sector validation of the technology."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-18",
        "notes": (
            "The project involved ESTCP and collaboration with DIU, "
            "the U.S. Air Force and U.S. Navy."
        ),
    },
    {
        "signal_id": "SIG-0020",
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "evidence_date": "2025-07-31",
        "evidence_type": "field_deployment",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction"
        ),
        "treatment_role": "destruction",
        "target_matrix": "AFFF",
        "maturity_or_deployment_stage": "government_demonstration",
        "partner_organizations": (
            "United States Army Corps of Engineers;"
            "National Defense Center for Energy and Environment"
        ),
        "location": "Vicksburg, Mississippi, United States",
        "source_title": (
            "Aquagga Mobilizes Steed Systems for U.S. Army Corps "
            "of Engineers AFFF Destruction Project"
        ),
        "source_url": (
            "https://www.aquagga.com/blog/"
            "aquagga-mobilizes-steed-systems-for-u-s-army-corps-of-engineers-"
            "afff-destruction-project"
        ),
        "source_type": "company_press_release",
        "evidence_summary": (
            "Aquagga mobilized two Steed Series HALT systems to the "
            "U.S. Army Corps of Engineers ERDC site in Mississippi for "
            "an AFFF destruction demonstration funded by NDCEE."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-18",
        "notes": (
            "The deployment used two systems operating in parallel, "
            "providing evidence of scaling and government-site operation."
        ),
    },
    {
        "signal_id": "SIG-0021",
        "organization_id": "ORG-005",
        "organization_name": "Aquagga, Inc.",
        "evidence_date": "",
        "evidence_type": "licensing",
        "technology_labels": (
            "hydrothermal_alkaline_treatment;"
            "hydrothermal_destruction"
        ),
        "treatment_role": "destruction",
        "target_matrix": "PFAS_contaminated_liquids",
        "maturity_or_deployment_stage": "technology_commercialization",
        "partner_organizations": (
            "Colorado School of Mines;"
            "University of Washington"
        ),
        "location": "United States",
        "source_title": "Hydrothermal Alkaline Treatment PFAS Destruction",
        "source_url": "https://www.aquagga.com/ourtech",
        "source_type": "company_technology_page",
        "evidence_summary": (
            "Aquagga states that it is the exclusive licensee of the "
            "foundational HALT patent from Colorado School of Mines and "
            "also holds an exclusive license to hydrothermal-processing "
            "intellectual property from the University of Washington."
        ),
        "confidence_level": "high",
        "verification_status": "verified_primary_source",
        "date_accessed": "2026-08-18",
        "notes": (
            "This signal captures the research-IP-to-startup "
            "commercialization pathway."
        ),
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