# Independent Relevance Classifier Holdout Validation

## Validation design

An independent stratified holdout sample of 50 records was reviewed
manually after the relevance classifier had been refined and frozen.

The sample contained 10 records from each predicted relevance category:

- `water_treatment`
- `adjacent_matrix`
- `treatment_unspecified_matrix`
- `contextual`
- `likely_irrelevant`

The 50 holdout records did not overlap with the 25-record development
validation sample.

## Overall result

- Total records reviewed: 50
- Exact-label matches: 40
- Exact-label accuracy: 80.0%
- Records manually included: 36
- Records manually excluded: 14

## Precision by predicted category

| Predicted category | Correct | Total | Precision |
|---|---:|---:|---:|
| `water_treatment` | 8 | 10 | 80.0% |
| `adjacent_matrix` | 8 | 10 | 80.0% |
| `treatment_unspecified_matrix` | 5 | 10 | 50.0% |
| `contextual` | 9 | 10 | 90.0% |
| `likely_irrelevant` | 10 | 10 | 100.0% |

## Classification errors

### Predicted `water_treatment`

- One broad PFAS symposium paper was manually classified as `contextual`.
- One phytomanagement study targeting contaminated land was manually
  classified as `adjacent_matrix`.

### Predicted `adjacent_matrix`

- One sewage-sludge hydrochar study was manually classified as
  `likely_irrelevant`.
- One broad overview of PFAS uses was manually classified as `contextual`.

### Predicted `treatment_unspecified_matrix`

- Four records were manually classified as `water_treatment`.
- One record was manually classified as `adjacent_matrix`.

All records in this category remained relevant enough for inclusion.

### Predicted `contextual`

- One broad wildlife contaminant-screening study was manually classified
  as `likely_irrelevant`.

### Predicted `likely_irrelevant`

All 10 records were confirmed as `likely_irrelevant` and excluded.

## Interpretation

The classifier performs well as a relevance-screening and prioritisation
tool for the PFAS technology-landscape corpus.

The `water_treatment`, `adjacent_matrix`, and `contextual` categories show
good precision on unseen records.

The `treatment_unspecified_matrix` category has lower exact-label precision,
but it functions effectively as a manual-review queue. Its errors were all
reassignments to other relevant treatment categories rather than false
inclusions of irrelevant records.

The `likely_irrelevant` category showed 100% precision in this holdout
sample. It can be used to prioritise candidate exclusions, although records
should not be irreversibly deleted without review.

## Recommended operational use

- Use `water_treatment` as the primary analysis corpus.
- Retain `adjacent_matrix` for secondary treatment and residual-management
  analysis.
- Manually screen every `treatment_unspecified_matrix` record.
- Selectively retain `contextual` records for background and interpretation.
- Treat `likely_irrelevant` as a high-confidence candidate-exclusion group.
