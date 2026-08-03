# Relevance Classifier Validation

## Validation design

A stratified sample of 25 records was reviewed manually.

The sample contained five records from each automatic relevance category:

- `water_treatment`
- `adjacent_matrix`
- `treatment_unspecified_matrix`
- `contextual`
- `likely_irrelevant`

## Overall result

- Total records reviewed: 25
- Exact-label matches: 21
- Exact-label accuracy: 84.0%
- Records manually included: 20
- Records manually excluded: 5

## Precision by automatic category

| Automatic category | Correct | Total | Precision |
|---|---:|---:|---:|
| `water_treatment` | 4 | 5 | 80.0% |
| `adjacent_matrix` | 5 | 5 | 100.0% |
| `treatment_unspecified_matrix` | 3 | 5 | 60.0% |
| `contextual` | 5 | 5 | 100.0% |
| `likely_irrelevant` | 4 | 5 | 80.0% |

## Observed errors

1. One sludge-treatment record was classified as `water_treatment`
   because wastewater-related terminology obscured the actual solid matrix.

2. One spent-sorbent study was classified as
   `treatment_unspecified_matrix` rather than `adjacent_matrix`.

3. One lubricant review was classified as
   `treatment_unspecified_matrix` rather than `contextual`.

4. One PFAS disposal review was classified as
   `likely_irrelevant` rather than `contextual`.

## Interpretation

The classifier performs well as a screening and prioritisation tool.

Most errors occurred between neighbouring relevance categories rather than
between clearly relevant and clearly irrelevant records.

The `treatment_unspecified_matrix` category acts as a useful manual-review
queue, although its exact-label precision is lower than the other categories.

The `likely_irrelevant` category should be treated as a candidate-exclusion
group rather than being deleted automatically.

## Recommended use

- Prioritise `water_treatment` records for core analysis.
- Retain `adjacent_matrix` records for secondary analysis.
- Manually screen `treatment_unspecified_matrix`.
- Selectively retain `contextual` records.
- Review `likely_irrelevant` records before final exclusion.
