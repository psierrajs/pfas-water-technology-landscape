# Project Status

## Current phase

Portfolio packaging and final project review.

## Overall status

Core analysis complete. Portfolio preparation in progress.

## Completed

### Project design and methodology

- Defined the primary research question and secondary intelligence questions.
- Defined the geographic and time scope.
- Documented the initial technology taxonomy.
- Defined inclusion and exclusion criteria.
- Documented the exploratory methodology.
- Documented copyright, licensing and confidentiality precautions.
- Created the reproducible repository structure.
- Configured Git and GitHub version control.
- Created the Python environment and project dependencies.

### Scientific literature analysis

- Designed and documented the OpenAlex scientific-literature search strategy.
- Tested broad and technology-specific retrieval approaches.
- Built a reference set for recall testing.
- Implemented DOI-based recall validation.
- Identified recall gaps in single broad-query retrieval.
- Combined broad and technology-specific searches.
- Created a deduplicated analysis-ready scientific corpus.
- Produced a final corpus of 658 records covering 2018–2026.
- Classified records by relevance and technology.
- Analysed annual publication growth.
- Analysed technology-specific momentum.
- Analysed institution–technology momentum.
- Enriched authorship and institutional metadata.
- Corrected institutional aliases and affiliation-resolution errors.
- Analysed institutional and international collaboration networks.
- Classified evidence type and maturity.
- Manually validated high-maturity pilot, field and full-scale records.

### Patent intelligence

#### Activated carbon

- Performed and documented a Google Patents pilot search.
- Screened 67 publication records.
- Consolidated records into 45 patent families.
- Performed manual family-quality assurance.
- Retained 25 relevant patent families.
- Classified treatment mode, carbon type, PFAS handling, system configuration, maturity and strategic theme.
- Generated activated-carbon patent intelligence reports and figures.

#### Ion exchange

- Designed and documented a PATENTSCOPE search strategy.
- Exported and processed 49 patent records.
- Completed title and IPC screening.
- Reviewed uncertain records.
- Consolidated the final screening decisions.
- Produced a provisional family-level dataset.
- Retained 17 relevant patent families.
- Classified treatment mode and resin strategy.
- Generated the ion-exchange patent intelligence report.

#### Electrochemical oxidation

- Completed an electrochemical-oxidation patent pilot.
- Screened 22 patent publications.
- Retained 15 relevant patent families.
- Identified recent priority-date activity.
- Identified academic and commercial assignees.
- Generated the electrochemical-oxidation patent pilot report.

### Cross-technology analysis

- Compared activated-carbon and ion-exchange patent portfolios.
- Compared treatment modes across technologies.
- Integrated scientific-publication and patent-family signals.
- Created a science–patent comparison figure.
- Identified capture, regeneration, concentration and destruction patterns across technologies.

### Technology assessment and strategic intelligence

- Assessed the scientific and applied position of:
  - activated carbon;
  - ion exchange;
  - electrochemical oxidation;
  - hydrothermal treatment;
  - supercritical water oxidation;
  - plasma;
  - photocatalysis;
  - sonolysis;
  - biological treatment.
- Identified institutional programmes with coherent science-to-application trajectories.
- Identified public-sector, academic and engineering collaboration signals.
- Developed the strategic treatment architecture:

  **capture → concentrate → regenerate where possible → destroy**

### Reporting and reproducibility

- Created intermediate reports for the principal analytical stages.
- Generated reproducible figures from processed datasets.
- Completed a first full version of the final technology landscape report.
- Added:
  - Executive Summary;
  - Scientific Landscape;
  - Patent Landscape;
  - Cross-Technology Patent Comparison;
  - Science–Patent Integration;
  - Technology Assessment;
  - Strategic Findings;
  - Limitations;
  - Conclusions;
  - Reproducibility.
- Completed an editorial and terminology review of the final report.
- Updated the README to present the project as a portfolio-ready intelligence project.

## Commercial intelligence extension

The v1.1 commercial-intelligence layer is now operational as a pilot.

Current scope:

- 5 organizations
- 21 structured commercial signals
- organization intelligence profiles
- cross-company commercial comparison
- commercialization-model analysis
- signal-volume versus organization-coverage methodology
- competitive-intelligence monitoring framework

The pilot currently includes Battelle, Gradiant, Arcadis, Evoqua/Xylem and Aquagga.

The next phase should expand organization coverage and begin automating monitoring of deployments, contracts, partnerships, licensing, acquisitions, validation events and commercialization changes.

The current pilot is not intended to provide a quantitative ranking of companies or market leadership.

## Key outputs

- `README.md`
- `reports/final-technology-landscape.md`
- `reports/publication-trends-initial-findings.md`
- `reports/technology-growth-initial-findings.md`
- `reports/institution-technology-momentum-initial-findings.md`
- `reports/institutional-collaboration-initial-findings.md`
- `reports/high-maturity-validation-summary.md`
- `reports/patent-adsorption-pilot-summary.md`
- `reports/patent-adsorption-intelligence-summary.md`
- `reports/patent-ion-exchange-intelligence-summary.md`
- `reports/patent-eox-pilot-summary.md`
- `reports/patent-technology-comparison.md`
- `reports/science-patent-technology-comparison.md`
- `figures/patent_adsorption_strategic_themes.png`
- `figures/science_patent_technology_comparison.png`
- documented scientific and patent search strategies
- reusable Python scripts in `src/`

## Current methodological decisions

- The project is an exploratory technology-intelligence landscape rather than an exhaustive systematic review.
- The primary scientific-analysis period is 2018–2026.
- Coverage is global, with emphasis on Europe and North America.
- Scientific publications and patents form the main evidence base of the current version.
- Corporate, market and business intelligence are considered future extensions rather than fully completed evidence streams.
- Capture and destruction technologies are analysed separately where possible.
- Technology categories may overlap.
- Interpretable and reproducible analysis is prioritised over opaque scoring.
- Publication counts, patent-family counts and maturity signals are interpreted as complementary rather than directly equivalent indicators.
- Patent searches are technology-specific pilots and should not be treated as exhaustive freedom-to-operate analyses.
- Manual validation is used where automated classification is insufficient.
- Restricted or licensed raw data are not committed to the public repository.
- Python scripts are preferred over manual editing for derived analytical outputs.

## Remaining work before portfolio v1.0

- Create a one-page executive brief.
- Review `PROJECT_STATUS.md`, README and repository navigation as a first-time GitHub visitor.
- Verify that key reports, figures and search strategies are easy to locate.
- Perform a final repository-level quality check.
- Optionally add a compact technology-comparison table or visual summary if it improves readability.
- Tag or otherwise mark the first portfolio-ready release.

## Future extensions

Potential future work includes:

- additional patent landscapes for membranes, plasma, SCWO or other technologies;
- systematic commercial and company intelligence;
- funding, partnership and procurement analysis;
- automated monitoring of new publications and patents;
- organization and technology change detection;
- reusable competitive-intelligence dashboards;
- extension of the workflow to other scientific and industrial technology landscapes.

## Next step

Create the one-page executive brief and complete final portfolio packaging.

## Last updated

2026-08-09