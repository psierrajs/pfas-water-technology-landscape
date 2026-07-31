# Project Status

## Current phase

Scientific literature search development and pilot screening.

## Overall status

In progress.

## Completed

* Created the local project repository.
* Initialised Git using `main` as the default branch.
* Created the initial `.gitignore`.
* Created the initial project documentation files.
* Defined the primary research question.
* Defined the secondary intelligence questions.
* Documented the initial technology taxonomy.
* Defined the geographic and time scope.
* Documented the initial methodology.
* Defined initial inclusion and exclusion criteria.
* Documented copyright, licensing and confidentiality precautions.
* Created the initial repository directory structure.
* Added placeholder files to preserve empty directories in Git.
* Created placeholder files for the scientific literature and patent search strategies.
* Documented the initial scientific literature search strategy.
* Defined the initial PFAS, water and treatment concept blocks.
* Identified preliminary technology-specific search terminology.
* Performed a pilot search using the OpenAlex web interface.
* Reviewed an initial sample of search results.
* Defined preliminary publication-screening categories.
* Refined the initial inclusion and exclusion decisions.

## Current files

* `README.md`
* `PROJECT_STATUS.md`
* `research-question.md`
* `methodology.md`
* `.gitignore`
* `search-strategies/scientific-literature.md`
* `search-strategies/patents.md`
* `data/raw/`
* `data/processed/`
* `notebooks/`
* `src/`
* `figures/`
* `reports/`

## Current methodological decisions

* The study is exploratory rather than exhaustive.
* The primary analysis period is 2018–2026.
* Coverage is global, with particular attention to Europe, the United States and Canada.
* Evidence will be gathered from scientific publications, patents, corporate sources, research projects and business news.
* Capture and destruction technologies will be distinguished.
* Interpretable intelligence analysis will be prioritised before machine learning, RAG or LLM workflows.
* Restricted raw data and licensed database exports will not be published on GitHub.
* Review articles will be retained and classified separately from experimental studies.
* Studies of degradation products will be included when they directly evaluate a treatment process.
* Analytical and monitoring studies without a treatment component will normally be excluded.
* Broad retrieval followed by title and abstract screening is preferred over aggressive query exclusions.

## Next step

Design a reproducible OpenAlex API query and retrieve a small metadata sample for screening.

## Known issues and open questions

* The provisional technology taxonomy will need validation against the terminology found in the literature and patents.
* The exact fields for the processed dataset have not yet been finalised.
* Patent family handling and organisation-name normalisation methods still need to be defined.
* Public data-source licences and redistribution conditions must be reviewed before publishing datasets.
* The distinction between analytical studies and treatment-performance studies may require manual judgement.
* The initial OpenAlex query syntax and metadata fields still need to be tested.

## Last updated

2026-07-31
