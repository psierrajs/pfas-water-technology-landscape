# Project Status

## Current phase

Scientific literature search validation and OpenAlex recall testing.

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
* Created a Python virtual environment for the project.
* Added `requests` as the first project dependency.
* Created `requirements.txt` and `.env.example`.
* Configured the OpenAlex API key locally without exposing it to Git.
* Created the first reproducible OpenAlex query script.
* Successfully retrieved and screened an initial sample of ten records.
* Documented the initial OpenAlex API test and its screening results.
* Created an initial scientific literature reference set.
* Classified ten relevant publications by technology category.
* Added independently discovered membrane and photocatalysis references.
* Created a reusable DOI-based recall-checking script.
* Confirmed that the membrane reference appears at position 64.
* Confirmed that the photocatalysis reference appears at position 113.
* Documented the effect of ranking on apparent search recall.
* Added an independent sonolysis reference to the scientific literature reference set.
* Confirmed that the sonolysis reference was not found within the first 500 results of the broad query.
* Confirmed that the same reference appeared at position 8 in a technology-specific sonolysis query.
* Identified a practical recall gap in the single-query search design.
* Added an independent supercritical water oxidation reference.
* Confirmed retrieval at position 52 in the broad query and position 1 in the technology-specific query.
* Fixed case-sensitive DOI comparison in the recall-testing script.
* Added an independent catalyzed hydrothermal liquefaction reference.
* Confirmed that it was not found within the first 500 broad-query results.
* Confirmed retrieval at position 3 in the technology-specific query.

## Current files

* `README.md`
* `PROJECT_STATUS.md`
* `research-question.md`
* `methodology.md`
* `.gitignore`
* `.env.example`
* `requirements.txt`
* `search-strategies/scientific-literature.md`
* `search-strategies/reference-set.md`
* `search-strategies/patents.md`
* `src/search_openalex.py`
* `src/check_reference_recall.py`
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
* API credentials will be stored only in the local `.env` file.
* Initial OpenAlex queries will retrieve small samples before any large-scale collection.
* Search performance will be assessed using both precision and recall.
* Known relevant records will be used to test whether the query misses important technologies.
* Recall testing will use DOI-based validation and paginated result inspection.
* Small result samples are not sufficient to judge technology coverage because relevant records may rank substantially lower.
* Technology-specific searches will be used to identify underrepresented categories and strengthen the reference set.
* The literature search will combine one broad query with technology-specific queries.
* Technology-specific queries are required where the broad query shows inadequate practical recall.
* Results from multiple queries will need DOI-based or OpenAlex-ID-based deduplication.

## Next step

Identify and test an independent reference for catalytic PFAS degradation or a combined capture-and-destroy process.

## Known issues and open questions

* The provisional technology taxonomy will need validation against the terminology found in the literature and patents.
* The exact fields for the processed dataset have not yet been finalised.
* Patent family handling and organisation-name normalisation methods still need to be defined.
* Public data-source licences and redistribution conditions must be reviewed before publishing datasets.
* The distinction between analytical studies and treatment-performance studies may require manual judgement.
* The OpenAlex query syntax and metadata fields still need further testing.
* The reference set remains small and is not statistically representative.
* Several destructive and combined technology categories remain absent from the reference set.
* The first search script prints records but does not yet save structured metadata.
* Error handling and query configuration will need improvement before larger retrievals.
* Ranking differences may bias conclusions if only small result windows are analysed.
* The number and scope of technology-specific queries still need to be defined.
* A reproducible deduplication method will be required when combining query results.

## Last updated

2026-08-01
