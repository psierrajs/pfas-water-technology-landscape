# Scientific Literature Search Strategy

## 1. Search objective

The objective of this search is to identify scientific publications relevant to emerging technologies for the removal, separation, concentration, degradation, destruction or mineralisation of PFAS in water.

The search will support analysis of:

- publication activity over time;
- activity by technology category;
- leading authors and research organisations;
- geographic distribution;
- collaboration patterns;
- links between scientific research and technological or commercial development;
- evidence of progression from laboratory research towards pilot or applied deployment.

The search is intended for an exploratory scientific and technology intelligence study. It is not designed as an exhaustive systematic review.

## 2. Scope

### Time period

The primary publication period is 2018–2026.

Earlier publications may be retained when they:

- describe a foundational treatment approach;
- are frequently cited by later work;
- help explain the development of an emerging technology;
- provide historical context for an organisation or research programme.

### Geographic coverage

The search will have global coverage.

Geographic analysis will place particular emphasis on:

- Europe;
- United States;
- Canada.

### Document types

The initial search will prioritise:

- journal articles;
- review articles;
- conference papers where sufficient metadata is available.

Other document types may be considered later if they provide useful evidence of technology development.

## 3. Conceptual search structure

The core search logic will combine three concept blocks:

1. PFAS terminology;
2. water or aqueous-environment terminology;
3. treatment, removal, separation or destruction terminology.

The general structure is:

```text
PFAS terms
AND
water or aqueous-system terms
AND
treatment or destruction terms
```

```

Technology-specific terms will later be used to classify records or construct targeted searches for individual technology categories.

## 4. Initial concept blocks

### Block A — PFAS terminology

Candidate terms include:

- PFAS
- "per- and polyfluoroalkyl substances"
- "perfluoroalkyl substances"
- "polyfluoroalkyl substances"
- PFOA
- PFOS
- GenX
- PFHxS
- PFNA
- PFBS

Additional substance names and abbreviations may be added after reviewing terminology in relevant publications.

### Block B — Water and aqueous systems

Candidate terms include:

- water
- wastewater
- groundwater
- drinking water
- surface water
- aqueous
- water treatment
- water remediation
- landfill leachate
- industrial effluent
- contaminated water

### Block C — Treatment and technology activity

Candidate terms include:

- treatment
- removal
- remediation
- separation
- capture
- adsorption
- concentration
- degradation
- destruction
- decomposition
- mineralisation
- mineralization
- defluorination

## 5. Technology-specific terminology

The following terms will be explored for targeted searching and classification:

### Adsorption

- activated carbon
- granular activated carbon
- powdered activated carbon
- ion exchange
- ion-exchange resin
- biochar
- porous material
- metal-organic framework
- covalent organic framework

### Membranes

- reverse osmosis
- nanofiltration
- membrane separation
- functionalised membrane
- functionalized membrane

### Destructive technologies

- electrochemical oxidation
- electrochemical degradation
- plasma treatment
- non-thermal plasma
- photocatalysis
- photochemical degradation
- sonolysis
- ultrasound
- supercritical water oxidation
- hydrothermal treatment
- thermal treatment
- catalytic degradation

### Combined processes

- treatment train
- combined process
- hybrid process
- capture and destroy
- membrane concentration
- concentrate treatment

## 6. Initial data sources

The first reproducible search will use OpenAlex because it provides openly accessible scholarly metadata and an API suitable for Python-based analysis.

Other sources may later be used for validation or supplementary searching, including:

- OpenAlex;
- Crossref;
- PubMed;
- institutional repositories;
- Google Scholar for limited manual discovery;
- Scopus or Web of Science where authorised access is available.

Searches performed in subscription databases will be documented, but restricted exports or licensed metadata will not be uploaded to the public repository.

## 7. Next development step

The next step is to design and test a broad OpenAlex search, review a small sample of retrieved records, and refine the terminology based on false positives and missed relevant records.

## 8. Pilot search

### Search date

2026-07-31

### Source

OpenAlex web interface.

### Initial query

```text
PFAS water treatment
```

### Filters

* Publication years: 2018–2026
* Global coverage
* No document-type restriction applied during the initial review

### Purpose

The purpose of this pilot search was to assess the relevance of a simple natural-language query before designing a reproducible API-based search.

### Initial observations

The first results included several highly relevant technology reviews and experimental treatment studies.

Relevant review articles covered:

* emerging PFAS water-treatment technologies;
* separation and degradation technologies;
* comparisons of currently available remediation technologies;
* next-generation water-treatment approaches.

Relevant experimental studies included:

* electrochemical oxidation at pilot scale;
* plasma-based PFAS degradation;
* activated carbon and anion-exchange treatment;
* plasma degradation and analysis of transformation products.

The search also retrieved publications focused primarily on PFAS analysis and monitoring across the urban water cycle. These records may mention water treatment but do not necessarily evaluate a treatment technology.

### Preliminary record categories

The pilot search suggests that records should initially be classified as:

* experimental treatment study;
* technology review;
* analytical or monitoring study;
* occurrence or environmental-fate study;
* pilot or demonstration study;
* other or unclear.

### Preliminary inclusion decision

Include records that:

* evaluate a PFAS removal, separation, concentration or destruction process;
* review technologies for PFAS treatment;
* examine degradation products generated by a treatment process;
* describe pilot-scale or applied treatment activity.

Exclude records that:

* focus only on PFAS detection or analytical methodology;
* report occurrence without evaluating treatment;
* focus on toxicology, regulation or environmental fate without a treatment component.

### Lessons for query development

The phrase `water treatment` retrieves many relevant records but does not reliably exclude analytical studies.

A broad search should therefore be followed by title and abstract screening rather than relying exclusively on restrictive query terms. Overly narrow exclusions may remove relevant studies that examine treatment performance through degradation products or analytical measurements.

## 9. Initial OpenAlex API test

### Test date

2026-07-31

### Endpoint

```text
https://api.openalex.org/works
```

### Parameters

```text
search=PFAS water treatment
filter=from_publication_date:2018-01-01,to_publication_date:2026-12-31
per-page=10
```

The API key was supplied locally through the `OPENALEX_API_KEY` environment variable and was not stored in the source code or committed to Git.

### Implementation

The initial query was implemented in:

```text
src/search_openalex.py
```

The script:

* loads the API key from a local `.env` file;
* sends a request to the OpenAlex works endpoint;
* restricts publication dates to 2018–2026;
* retrieves ten records;
* prints the title, publication year and DOI;
* does not yet save records to disk.

### Initial screening results

Of the first ten records:

* seven were clearly relevant treatment studies or technology reviews;
* one was relevant but combined PFAS occurrence with drinking-water treatment;
* one concerned the general uses of PFAS and was considered a clear false positive;
* one focused primarily on analytical workflows and was considered a probable exclusion.

This represents an initial estimated relevance of approximately eight records out of ten.

### Interpretation

The natural-language query provides good initial precision and retrieves multiple technology categories, including:

* adsorption;
* ion exchange;
* plasma treatment;
* electrochemical oxidation;
* separation and degradation technologies.

However, the query also retrieves records in which PFAS and water-treatment terminology appear without a direct technology-treatment focus.

The next query-development step should assess recall by testing whether known relevant studies are missed, rather than optimising precision solely from the first ten results.

