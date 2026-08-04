# Initial Evidence-Type Classification Analysis

## Purpose

This analysis classifies PFAS water-treatment publications by the type of evidence they provide.

The objective is to distinguish between:

* reviews and state-of-the-field syntheses;
* clearly experimental studies;
* mechanistic studies;
* computational studies;
* pilot-scale work;
* field demonstrations;
* life-cycle assessments;
* publications whose evidence type cannot be determined confidently from the title.

The classification is intended to support later assessment of technology maturity and movement from laboratory research toward pilot and field application.

## Input corpus

The classifier uses:

`data/processed/openalex_analysis_corpus.csv`

The source corpus contains 658 deduplicated publications.

Only publications in the following analysis tiers were classified:

* `core`;
* `secondary`;
* `manual_review`.

This produced 449 classified publications.

Background and exclude-candidate records were not included in the evidence-type analysis.

## Classification categories

The current classifier uses the following primary categories:

* `field_demonstration`;
* `pilot`;
* `techno_economic`;
* `life_cycle_assessment`;
* `review`;
* `computational`;
* `mechanistic`;
* `experimental`;
* `laboratory`;
* `other`.

## Classification logic

The classifier uses ordered regular-expression rules.

The primary evidence type is determined from signals that appear explicitly in the publication title.

This title-first design was adopted after testing showed that using abstract text for the primary label produced too many false positives.

For example:

* review articles mentioning full-scale applications were incorrectly classified as field demonstrations;
* general papers mentioning pilot studies in the abstract were incorrectly classified as pilot-scale evidence;
* reviews discussing laboratory experiments were classified as laboratory studies;
* broad treatment papers were classified as mechanistic because their abstracts mentioned mechanisms or pathways.

The final rule set therefore prioritizes precision over coverage.

The title determines the primary label, while the combined title and abstract are still used to record secondary evidence signals.

The output retains:

* `primary_evidence_type`;
* `evidence_types`;
* `evidence_type_count`;
* `evidence_signals`;
* `evidence_method`.

The method identifier is:

`rule_based_v3_title_primary`

## Final primary classification results

| Primary evidence type | Publications |
| --------------------- | -----------: |
| Other                 |          291 |
| Review                |          101 |
| Experimental          |           30 |
| Computational         |            9 |
| Mechanistic           |            7 |
| Pilot                 |            6 |
| Field demonstration   |            3 |
| Life-cycle assessment |            2 |
| Techno-economic       |            0 |
| Laboratory            |            0 |
| **Total**             |      **449** |

## Interpretation of the distribution

The large `other` category is intentional.

It means that the title did not contain a sufficiently explicit signal to assign a more specific evidence type automatically.

This is preferable to forcing uncertain publications into categories such as experimental, mechanistic, pilot or field demonstration.

The classifier should therefore be interpreted as a high-precision screening tool rather than a complete evidence taxonomy.

The current results are especially useful for identifying the small number of publications that make explicit claims about:

* pilot-scale treatment;
* field demonstration;
* life-cycle assessment;
* computational modelling;
* experimental validation;
* mechanistic investigation.

## Conservative treatment of laboratory evidence

The `laboratory` category currently contains zero publications.

This does not mean that the corpus contains no laboratory studies.

Instead, it reflects the conservative rule that a publication must explicitly include title terms such as:

* laboratory-scale;
* lab-scale;
* bench-scale;
* batch experiment;
* column experiment.

Most experimental PFAS treatment papers do not state the laboratory scale directly in their titles.

They are therefore classified as `experimental` when the title contains a stronger technical signal, or as `other` when it does not.

The category has been retained for future use, but it should not currently be interpreted as a measure of total laboratory activity.

## Validated high-value evidence categories

### Field demonstrations

Three publications were classified as field demonstrations:

* 2020 — *Removal of per- and polyfluoroalkyl substances (PFASs) in a full-scale drinking water treatment plant: Long-term performance of granular activated carbon (GAC) and influence of flow-rate*
* 2021 — *Field demonstration of coupling ion-exchange resin with electrochemical oxidation for enhanced treatment of per- and polyfluoroalkyl substances (PFAS) in groundwater*
* 2024 — *Field Demonstration of PFAS Destruction in Various Alcohol-Resistant AFFFs Using Supercritical Water Oxidation (SCWO)*

These records are strategically important because they provide explicit evidence of treatment beyond conventional laboratory studies.

They cover:

* full-scale drinking-water treatment using granular activated carbon;
* field deployment of ion exchange coupled with electrochemical oxidation;
* field demonstration of supercritical water oxidation for AFFF destruction.

The 2021 and 2024 publications are especially relevant to the project’s capture-and-destroy and destructive-treatment themes.

### Pilot-scale studies

Six publications were classified as pilot-scale evidence:

* 2019 — *Rapid Removal of Poly- and Perfluorinated Compounds from Investigation-Derived Waste (IDW) in a Pilot-Scale Plasma Reactor*
* 2022 — *Comparative investigation of PFAS adsorption onto activated carbon and anion exchange resins during long-term operation of a pilot treatment plant*
* 2022 — *Using Electrochemical Oxidation to Remove PFAS in Simulated Investigation-Derived Waste (IDW): Laboratory and Pilot-Scale Experiments*
* 2023 — *Electrochemical Oxidation for Treatment of PFAS in Contaminated Water and Fractionated Foam─A Pilot-Scale Study*
* 2024 — *A non-target evaluation of drinking water contaminants in pilot scale activated carbon and anion exchange resin treatments*
* 2025 — *Pilot scale treatment of PFAS-contaminated groundwater in a subsurface flow constructed wetland–evaluating multiple plant species*

The pilot records span several technology families:

* plasma;
* activated carbon;
* ion exchange;
* electrochemical oxidation;
* constructed wetlands.

This diversity suggests that movement toward larger-scale evaluation is not limited to one treatment route.

### Life-cycle assessment

Two titles explicitly report life-cycle assessment:

* 2022 — *Environmental Life Cycle Assessment (LCA) of Treating PFASs with Ion Exchange and Electrochemical Oxidation Technology*
* 2023 — *Life cycle assessment and life cycle cost analysis of anion exchange and granular activated carbon systems for remediation of groundwater contaminated by per- and polyfluoroalkyl substances (PFASs)*

Both studies focus on established capture technologies and, in one case, integration with electrochemical oxidation.

They provide evidence that PFAS treatment evaluation is expanding beyond removal efficiency toward broader environmental and cost implications.

### Computational evidence

Nine publications were classified as computational based on explicit title signals such as:

* simulation;
* molecular dynamics;
* first-principles calculations;
* density functional theory;
* machine learning;
* theoretical evaluation;
* kinetic modelling;
* in silico design.

Representative examples include:

* molecular simulation of PFAS removal by polyamide membranes;
* ReaxFF simulation of PFNA degradation by SCWO;
* kinetic modelling of PFAS pyrolysis and incineration;
* first-principles analysis of hydrated-electron degradation;
* DFT analysis of mechanochemical degradation;
* machine-learning analysis of electrochemical oxidation.

This category separates computational evidence from laboratory or field evidence while retaining mechanistic relevance through secondary labels.

## Experimental and mechanistic evidence

Thirty publications were classified as explicitly experimental.

These include title signals such as:

* validation;
* performance testing;
* reactor studies;
* anode or electrode studies;
* photocatalytic degradation;
* electrochemical degradation;
* plasma degradation;
* experimental investigation.

The category contains studies across:

* supercritical water oxidation;
* electrochemical oxidation;
* photocatalysis;
* plasma;
* adsorption;
* hydrothermal treatment;
* foam fractionation.

Seven publications were classified as mechanistic based on explicit title terms such as mechanism, pathway or kinetic insight.

This category is intentionally narrow.

Computational papers containing mechanistic analysis are classified primarily as computational when the title makes the modelling approach explicit.

Experimental papers with mechanistic secondary signals remain primarily experimental.

## Review classification

A total of 101 publications were classified as reviews.

The review rules recognize title terms including:

* review;
* meta-analysis;
* state of the art;
* state of the science;
* overview;
* recent progress;
* recent advances;
* technology status;
* progress and perspectives;
* research updates.

Review is given high priority in the title-based rules.

This prevents broad review papers from being incorrectly classified as field, pilot, mechanistic or experimental evidence merely because their abstracts discuss those topics.

## Classification development

Several versions of the rule set were tested.

### Initial combined-text rules

The first version used the combined title and abstract to determine the primary category.

This produced:

* 24 field demonstrations;
* 21 pilot studies;
* 4 laboratory studies;
* 232 other records.

Manual inspection revealed many false positives.

### Title-first refinement

The next version gave priority to explicit title signals but still used abstract matches when the title was inconclusive.

This reduced false positives but continued to misclassify:

* reviews as field demonstrations;
* reviews as laboratory studies;
* general papers as mechanistic studies;
* cost-related abstracts as techno-economic analyses.

### Final conservative version

The final version uses the title alone for the primary evidence type.

The abstract is retained only for secondary signals.

This reduced coverage but substantially improved interpretability and precision.

The resulting classifier should be regarded as a transparent, reproducible screening tool rather than an attempt to replace manual evidence assessment.

## Limitations

The primary category reflects title wording rather than full-text study design.

A publication may contain strong experimental evidence without using an explicit experimental term in its title.

The `other` category therefore contains many technically relevant publications.

The classifier does not yet distinguish:

* bench scale from laboratory scale;
* controlled laboratory work from real-water testing;
* pilot scale from demonstration scale when titles are ambiguous;
* treatment performance studies from material-synthesis studies;
* original research from conference proceedings;
* technology-readiness levels.

The rules also depend on English-language terminology.

The zero count for `techno_economic` should not be interpreted as evidence that no economic analysis exists in the corpus.

It means only that no title matched the current explicit techno-economic patterns after conservative classification.

## Strategic implications

The evidence analysis confirms that the corpus is dominated by reviews and studies whose evidence type cannot be identified automatically from the title.

Nevertheless, it contains a small but valuable group of publications demonstrating movement toward application:

* three field demonstrations;
* six pilot-scale studies;
* two life-cycle assessments;
* several explicit validation and reactor studies.

The strongest maturity signals identified so far include:

* full-scale GAC treatment;
* ion exchange coupled with electrochemical oxidation in groundwater;
* field demonstration of SCWO;
* pilot plasma treatment;
* pilot electrochemical oxidation;
* long-term pilot adsorption and ion-exchange treatment.

These records should be prioritized in later assessment of technology readiness, commercial activity and patent positioning.

## Recommended next steps

The next stage should:

1. manually validate all field and pilot records;
2. connect evidence type to technology labels;
3. identify institutions and companies associated with high-maturity evidence;
4. distinguish reviews from original research in momentum calculations;
5. create an evidence-type-by-technology matrix;
6. develop a manual-review protocol for high-value `other` records.

