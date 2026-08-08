# Patent Search Strategy — Ion-Exchange Resins for PFAS Water Treatment

## Objective

Identify patent publications related to the use of ion-exchange resins for the removal of PFAS from water, including drinking water, groundwater, wastewater, leachate, and other aqueous streams.

The search is intended to support a technology-intelligence landscape rather than a freedom-to-operate analysis.

## Scope

### Included concepts

- PFAS, PFOA, PFOS, perfluoroalkyl and polyfluoroalkyl substances
- water and aqueous treatment
- ion-exchange resins
- anion-exchange resins
- strong-base anion resins
- weak-base anion resins
- selective PFAS resins
- regenerable ion-exchange media
- resin-based adsorption and capture systems

### Excluded or secondary concepts

- activated carbon when ion exchange is not part of the invention
- membrane-only treatment
- purely destructive technologies without resin capture
- analytical or sensing applications
- fluoropolymer manufacture without water-treatment relevance

## Google Patents Query

### PAT-IX-001 — Broad ion-exchange resin search

```text
(
  TI=(PFAS OR PFOA OR PFOS OR "perfluoroalkyl" OR "polyfluoroalkyl")
  OR
  AB=(PFAS OR PFOA OR PFOS OR "perfluoroalkyl" OR "polyfluoroalkyl")
)
AND
(
  TI=(water OR groundwater OR wastewater OR leachate OR aqueous)
  OR
  AB=(water OR groundwater OR wastewater OR leachate OR aqueous)
)
AND
(
  TI=("ion exchange" OR "ion-exchange" OR "anion exchange"
      OR "anion-exchange" OR "exchange resin" OR "ion exchange resin"
      OR "anion exchange resin")
  OR
  AB=("ion exchange" OR "ion-exchange" OR "anion exchange"
      OR "anion-exchange" OR "exchange resin" OR "ion exchange resin"
      OR "anion exchange resin")
)

```
