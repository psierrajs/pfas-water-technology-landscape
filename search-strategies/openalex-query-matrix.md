# OpenAlex query matrix

## Purpose

This file records the first reproducible set of broad and technology-specific OpenAlex queries for the PFAS water technology landscape.

The strategy combines:

* one broad cross-technology query;
* targeted queries for individual technology categories;
* DOI-based recall testing against the independent reference set;
* later deduplication using DOI or OpenAlex Work ID.

## Scope

Publication years: 2018–2026

Primary context: PFAS treatment, removal, concentration or destruction in water and aqueous matrices.

## Broad query

| Query ID | Category | Query |
|---|---|---|
| B01 | Cross-technology | `PFAS water treatment` |

## Technology-specific queries

| Query ID | Category | Query |
|---|---|---|
| T01 | Adsorption | `PFAS adsorption water treatment` |
| T02 | Ion exchange | `PFAS ion exchange water treatment` |
| T03 | Membranes | `PFAS membrane filtration water` |
| T04 | Electrochemical oxidation | `PFAS electrochemical oxidation water` |
| T05 | Plasma | `PFAS plasma degradation water` |
| T06 | Photocatalysis | `PFAS photocatalytic degradation water` |
| T07 | Sonolysis | `PFAS sonolysis water degradation` |
| T08 | Supercritical water oxidation | `PFAS supercritical water oxidation` |
| T09 | Hydrothermal liquefaction | `PFAS hydrothermal liquefaction` |
| T10 | Capture-and-destroy | `PFAS combined adsorption electrochemical oxidation` |

## Initial recall observations

| Category | Broad-query result | Technology-specific result |
|---|---|---|
| Membranes | Found at position 64 | Not yet tested |
| Photocatalysis | Found at position 113 | Not yet tested |
| Sonolysis | Not found within first 500 | Found at position 8 |
| Supercritical water oxidation | Found at position 52 | Found at position 1 |
| Hydrothermal liquefaction | Not found within first 500 | Found at position 3 |
| Capture-and-destroy | Not found within first 500 | Found at position 28 |

## Interpretation

The broad query provides useful cross-technology coverage but does not retrieve all reference publications within a practical screening window.

Technology-specific queries substantially improve recall for several destructive and combined-treatment categories.

The final retrieval workflow should therefore:

1. execute the broad query;
2. execute every technology-specific query;
3. retain query provenance for each record;
4. merge all retrieved records;
5. deduplicate using DOI first and OpenAlex Work ID second;
6. record records retrieved by more than one query;
7. evaluate recall again after query refinement.

## Open questions

* Whether separate queries are needed for activated carbon, biochar and advanced porous materials.
* Whether reverse osmosis and nanofiltration should use separate membrane queries.
* Whether plasma variants require additional terms such as `cold plasma` or `non-thermal plasma`.
* Whether catalytic degradation should be separated from hydrothermal and electrochemical processes.
* Whether title-and-abstract field restrictions would improve precision.
* What practical result limit should be used for each query.
