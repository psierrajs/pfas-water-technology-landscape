# Patent Search Strategy

## Purpose

This patent search is designed to identify inventions, patent families, assignees and filing trends related to the removal, concentration, separation, destruction and treatment of per- and polyfluoroalkyl substances in water.

The patent analysis will support the broader research question:

> Which emerging technologies for PFAS removal or destruction in water show the strongest scientific, technological and commercial activity, and which organizations are best positioned?

## Scope

### Time period

Primary analysis period:

- 2018–2026

Earlier patents may be retained when they are:

- foundational;
- highly cited;
- members of active patent families;
- relevant to understanding the development of a technology.

### Geographic coverage

Global coverage, with particular attention to:

- United States;
- European Patent Office;
- World Intellectual Property Organization;
- Canada;
- Australia;
- Japan;
- South Korea;
- China.

### Document types

The analysis may include:

- patent applications;
- granted patents;
- international applications;
- patent families;
- utility patents.

Design patents and unrelated non-technical documents will be excluded.

## Technology scope

The search will cover the following technology groups:

### Capture and separation

- activated carbon;
- granular activated carbon;
- powdered activated carbon;
- ion-exchange resins;
- adsorbents;
- biochar;
- porous materials;
- metal-organic frameworks;
- membranes;
- reverse osmosis;
- nanofiltration;
- foam fractionation;
- separation and concentration systems.

### Destruction and degradation

- electrochemical oxidation;
- electrochemical degradation;
- plasma treatment;
- photocatalysis;
- sonolysis;
- supercritical water oxidation;
- hydrothermal treatment;
- thermal treatment;
- catalytic degradation;
- biological degradation.

### Combined systems

- capture and destroy;
- treatment trains;
- concentration followed by destruction;
- membrane concentrate treatment;
- resin regeneration combined with destruction;
- foam fractionation combined with destructive treatment.


## Core search concepts

The patent search will combine three concept blocks:

1. PFAS terminology;
2. water and aqueous-treatment terminology;
3. treatment-technology terminology.

### PFAS concept block

Core terms:

- PFAS;
- perfluoroalkyl;
- polyfluoroalkyl;
- per- and polyfluoroalkyl;
- perfluorinated compound;
- polyfluorinated compound;
- fluorinated surfactant;
- fluorochemical;
- organofluorine contaminant.

Named substances and classes may include:

- PFOA;
- PFOS;
- PFHxS;
- PFNA;
- PFBS;
- GenX;
- HFPO-DA;
- perfluorocarboxylic acid;
- perfluoroalkyl carboxylate;
- perfluoroalkane sulfonate;
- fluorotelomer;
- aqueous film-forming foam;
- AFFF.

### Water and environmental-treatment concept block

Core terms:

- water;
- drinking water;
- groundwater;
- wastewater;
- surface water;
- leachate;
- landfill leachate;
- contaminated water;
- aqueous stream;
- aqueous solution;
- industrial effluent;
- process water;
- remediation;
- water treatment;
- water purification;
- water decontamination.

### Treatment-technology concept block

Broad treatment terms:

- remove;
- removal;
- treat;
- treatment;
- separate;
- separation;
- adsorb;
- adsorption;
- degrade;
- degradation;
- destroy;
- destruction;
- oxidize;
- oxidation;
- mineralize;
- mineralization;
- defluorinate;
- defluorination;
- concentrate;
- concentration;
- regenerate;
- regeneration;
- remediate;
- remediation.

Technology-specific terms will be developed as separate search groups.

## Initial broad search logic

The broad search structure will be:

```text
(PFAS terminology)
AND
(water or aqueous-treatment terminology)
AND
(removal, separation, concentration, degradation or destruction terminology)
````

A generic example is:

```text
(
  PFAS
  OR perfluoroalkyl
  OR polyfluoroalkyl
  OR PFOA
  OR PFOS
  OR AFFF
)
AND
(
  water
  OR groundwater
  OR wastewater
  OR leachate
  OR aqueous
)
AND
(
  treatment
  OR removal
  OR adsorption
  OR separation
  OR degradation
  OR destruction
  OR oxidation
  OR remediation
)
```

This broad query will be used for recall-oriented exploration rather than as the final production query.

## Technology-specific search groups

Separate searches will be developed for:

* adsorption and activated carbon;
* ion exchange;
* advanced porous adsorbents;
* membranes;
* foam fractionation;
* electrochemical oxidation;
* plasma;
* photocatalysis;
* sonolysis;
* supercritical water oxidation;
* hydrothermal and thermal treatment;
* biological degradation;
* combined capture-and-destroy systems.

Each search group will combine PFAS terms with water terms and technology-specific terminology.

## Technology-specific terminology

### Adsorption and activated carbon

Example terms:

- activated carbon;
- granular activated carbon;
- powdered activated carbon;
- carbonaceous adsorbent;
- adsorption media;
- sorbent;
- adsorbent bed;
- biochar;
- carbon nanotube;
- graphene-based adsorbent.

Example logic:

```text
(PFAS terms)
AND
(water terms)
AND
(
  adsorb*
  OR sorbent
  OR "activated carbon"
  OR "granular activated carbon"
  OR "powdered activated carbon"
  OR biochar
)
````

### Ion exchange

Example terms:

* ion exchange;
* ion-exchange resin;
* anion-exchange resin;
* selective resin;
* regenerable resin;
* polymeric sorbent;
* resin regeneration.

Example logic:

```text
(PFAS terms)
AND
(water terms)
AND
(
  "ion exchange"
  OR "ion-exchange resin"
  OR "anion exchange resin"
  OR "selective resin"
  OR "resin regeneration"
)
```

### Advanced porous adsorbents

Example terms:

* metal-organic framework;
* MOF;
* covalent organic framework;
* COF;
* porous polymer;
* functionalized silica;
* molecularly imprinted polymer;
* cyclodextrin polymer;
* nanostructured adsorbent.

### Membranes

Example terms:

* membrane filtration;
* reverse osmosis;
* nanofiltration;
* ultrafiltration;
* membrane separation;
* functionalized membrane;
* selective membrane;
* membrane concentrate;
* retentate treatment.

Example logic:

```text
(PFAS terms)
AND
(water terms)
AND
(
  membrane
  OR "reverse osmosis"
  OR nanofiltration
  OR ultrafiltration
  OR retentate
  OR "membrane concentrate"
)
```

### Foam fractionation

Example terms:

* foam fractionation;
* foam separation;
* air fractionation;
* bubble fractionation;
* froth separation;
* surface-active contaminant separation;
* foamate;
* aeration separation.

### Electrochemical treatment

Example terms:

* electrochemical oxidation;
* electrooxidation;
* electrochemical degradation;
* anodic oxidation;
* electrocatalytic oxidation;
* electrochemical reactor;
* boron-doped diamond;
* BDD electrode;
* reactive electrochemical membrane.

Example logic:

```text
(PFAS terms)
AND
(water terms)
AND
(
  "electrochemical oxidation"
  OR electrooxidation
  OR "anodic oxidation"
  OR electrocatal*
  OR "boron-doped diamond"
  OR "reactive electrochemical membrane"
)
```

### Plasma treatment

Example terms:

* plasma treatment;
* non-thermal plasma;
* cold plasma;
* dielectric barrier discharge;
* gliding arc plasma;
* plasma reactor;
* plasma discharge;
* electrical discharge plasma.

### Photocatalysis

Example terms:

* photocatalysis;
* photocatalytic degradation;
* photochemical oxidation;
* ultraviolet degradation;
* UV treatment;
* titanium dioxide;
* TiO2;
* semiconductor photocatalyst;
* photoelectrocatalysis.

### Sonolysis

Example terms:

* sonolysis;
* ultrasonic degradation;
* ultrasound treatment;
* acoustic cavitation;
* sonochemical degradation;
* high-frequency ultrasound.

### Supercritical water oxidation

Example terms:

* supercritical water oxidation;
* SCWO;
* supercritical oxidation;
* supercritical water reactor;
* hydrothermal oxidation;
* wet oxidation.

### Hydrothermal and thermal treatment

Example terms:

* hydrothermal treatment;
* hydrothermal alkaline treatment;
* thermal decomposition;
* thermal destruction;
* pyrolysis;
* incineration;
* calcination;
* thermal mineralization;
* solvated electron treatment.

### Biological degradation

Example terms:

* biodegradation;
* biological treatment;
* microbial degradation;
* biotransformation;
* enzyme degradation;
* fungal treatment;
* bacterial degradation;
* constructed wetland;
* phytoremediation.

### Combined capture-and-destroy systems

Example terms:

* capture and destroy;
* treatment train;
* integrated treatment;
* sequential treatment;
* adsorption followed by destruction;
* concentration followed by oxidation;
* membrane concentration followed by destruction;
* resin regeneration and destruction;
* foam fractionation and destruction.

## Patent data sources

Potential patent data sources include:

- Google Patents;
- Espacenet;
- WIPO Patentscope;
- The Lens;
- USPTO Patent Center;
- EPO Open Patent Services;
- national patent-office databases where required.

The final workflow should prioritize sources that support:

- patent-family identification;
- assignee and applicant information;
- priority dates;
- publication and grant status;
- classification codes;
- citation data;
- machine-readable export where possible.

No single database should be assumed to provide complete coverage or perfectly normalized assignee data.

## Unit of analysis

The preferred unit of analysis will be the patent family rather than the individual publication.

This reduces duplication caused by the same invention being published in multiple jurisdictions.

Where possible, the analysis will retain:

- representative publication number;
- family identifier;
- earliest priority date;
- filing jurisdictions;
- applicant or assignee;
- inventor names;
- title;
- abstract;
- legal status;
- CPC and IPC classifications;
- cited and citing patents;
- technology labels;
- relevance decision.

Patent-family definitions may differ between databases. The source and family definition used must therefore be documented.

## Inclusion criteria

A patent record should be included when it:

- explicitly concerns PFAS, named PFAS compounds, fluorinated surfactants or AFFF;
- concerns treatment of water, wastewater, groundwater, leachate or another aqueous stream;
- describes removal, separation, concentration, degradation, destruction, mineralization, defluorination or regeneration;
- claims or describes a relevant treatment material, apparatus, process or integrated system;
- falls within the primary time scope or is retained as foundational context.

The patent does not need to contain the term `PFAS` when named substances such as PFOA, PFOS, GenX or fluorotelomers are clearly present.

## Exclusion criteria

A patent record should be excluded when it concerns:

- synthesis or manufacture of fluorinated chemicals without environmental treatment;
- fluoropolymer production;
- coatings, electronics, semiconductors or medical applications unrelated to water treatment;
- analytical detection without a treatment component;
- air or soil treatment with no meaningful aqueous-treatment application;
- general water purification with no PFAS relevance;
- patents mentioning PFAS only as incidental background;
- duplicate publications belonging to the same retained patent family.

Records with uncertain relevance should be retained for manual review rather than excluded automatically.

## Screening procedure

The initial screening process will use:

1. title review;
2. abstract review;
3. claim or description review where necessary;
4. patent-family consolidation;
5. applicant normalization;
6. technology classification;
7. manual relevance decision.

Suggested screening labels:

- `core`;
- `secondary`;
- `manual_review`;
- `exclude`.

Suggested inclusion decisions:

- `include`;
- `context_only`;
- `uncertain`;
- `exclude`.

## Technology classification

Patent families may receive more than one technology label.

Suggested labels include:

- `adsorption`;
- `ion_exchange`;
- `advanced_porous_adsorbent`;
- `membranes`;
- `foam_fractionation`;
- `electrochemical_oxidation`;
- `plasma`;
- `photocatalysis`;
- `sonolysis`;
- `supercritical_water_oxidation`;
- `hydrothermal`;
- `thermal`;
- `biological`;
- `capture_and_destroy`;
- `other`.

Multiple labels should be retained when an invention covers an integrated treatment train.

## Assignee normalization

Applicant and assignee names will require normalization because the same organization may appear under:

- abbreviations;
- subsidiaries;
- former names;
- spelling variants;
- national legal entities;
- university technology-transfer offices;
- joint applicants.

The normalized dataset should retain both:

- the original applicant name;
- the normalized organization name.

Corporate ownership changes should be recorded separately rather than silently replacing the historical applicant.

## Planned patent indicators

Potential indicators include:

- patent families by year;
- patent families by technology;
- leading applicants and assignees;
- applicant growth since 2018;
- geographic filing coverage;
- granted versus pending families;
- average family size;
- forward citations;
- collaboration between applicants;
- university–industry co-ownership;
- technology diversification by organization;
- overlap between scientific institutions and patent applicants;
- patent activity linked to pilot or commercial evidence.

These indicators will be interpreted cautiously because citation practices, publication delays and filing strategies vary across jurisdictions and technology fields.

## Limitations

The patent analysis may be affected by:

- an 18-month publication delay;
- incomplete or inconsistent legal-status data;
- variations in patent-family definitions;
- assignee-name inconsistencies;
- machine-translation errors;
- broad claims that extend beyond demonstrated applications;
- patents that mention PFAS without providing enabling treatment evidence;
- commercial secrecy and unpublished know-how;
- database-specific coverage and export limits.

Patent counts will not be treated as direct evidence of technical performance or commercial success.

## Search documentation and reproducibility

Every production search should be documented with:

- database or platform;
- date searched;
- exact query string;
- fields searched;
- language restrictions;
- jurisdiction restrictions;
- publication-date restrictions;
- number of results retrieved;
- export format;
- notes on database limitations.

Searches should be assigned stable identifiers, for example:

- `PAT-BROAD-001`;
- `PAT-ADS-001`;
- `PAT-IX-001`;
- `PAT-MEM-001`;
- `PAT-EOX-001`;
- `PAT-SCWO-001`.

Each exported record should retain the query identifier that retrieved it.

## Initial patent dataset fields

The initial raw patent dataset should aim to include:

- `record_id`;
- `query_id`;
- `publication_number`;
- `application_number`;
- `family_id`;
- `title`;
- `abstract`;
- `earliest_priority_date`;
- `publication_date`;
- `grant_date`;
- `applicant_original`;
- `assignee_original`;
- `inventors`;
- `jurisdictions`;
- `legal_status`;
- `ipc_codes`;
- `cpc_codes`;
- `forward_citations`;
- `backward_citations`;
- `source_database`;
- `source_url`.

The processed dataset should additionally include:

- `normalized_assignee`;
- `technology_labels`;
- `relevance_label`;
- `inclusion_decision`;
- `manual_review_required`;
- `family_representative`;
- `commercial_signal`;
- `notes`.

## Immediate next step

The next stage will be a small exploratory search rather than a full-scale download.

The initial pilot search should:

1. use a broad PFAS-water-treatment query;
2. retrieve a manageable sample;
3. inspect the main false-positive categories;
4. identify useful CPC and IPC classifications;
5. refine terminology for the first production search;
6. test whether patent-family and assignee data can be exported reliably.

The pilot search should be documented before expanding to the full patent landscape.


