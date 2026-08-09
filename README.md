# PFAS Water Technology Landscape

An exploratory and reproducible scientific, technology and competitive intelligence project focused on emerging technologies for the removal and destruction of PFAS in water.

## Research question

Which emerging technologies for PFAS removal or destruction in water show the strongest scientific, technological and business activity, and which organisations appear best positioned?

## Scope

- Period: 2018–2026
- Geographic coverage: global, with particular attention to Europe and North America
- Primary evidence analysed: scientific publications and patents
- Additional intelligence sources considered for future extension: corporate websites, research projects and business news
- Intended audience: an R&D director or innovation manager evaluating technologies, investments or potential collaborations

Sí, aquí podemos hacer algo muy útil en 15 minutos: **actualizar el README para que deje de parecer un proyecto recién empezado**.

Ahora mismo tiene dos problemas claros:

* dice `Planned outputs`, cuando muchos outputs ya existen;
* dice que el proyecto está en “methodology and repository setup phase”, lo cual ya no es cierto.

Yo sustituiría **desde `## Planned outputs` hasta el final** por esto:

````markdown
## Key findings

The current landscape combines scientific literature, patent analysis, maturity evidence and institutional collaboration signals.

Key findings include:

- Adsorption is the dominant scientific technology category in the analysed corpus.
- Activated carbon and ion exchange remain important mature capture technologies.
- Electrochemical oxidation shows strong scientific momentum together with pilot, field and recent patent signals.
- Supercritical water oxidation shows notable application maturity relative to its smaller scientific base.
- The strongest cross-cutting pattern is the emergence of integrated treatment architectures based on:

  **capture → concentrate → regenerate where possible → destroy**

## Main outputs

- [Final technology landscape report](reports/final-technology-landscape.md)
- Documented scientific and patent search strategies
- Reproducible Python analysis scripts
- Scientific publication and technology-trend analysis
- Institutional and collaboration analysis
- Technology-maturity assessment
- Activated-carbon patent landscape
- Ion-exchange patent landscape
- Electrochemical-oxidation patent pilot
- Cross-technology patent comparison
- Science–patent integration
- Reproducible figures and intermediate reports

## Repository structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── figures/
├── notebooks/
├── reports/
├── search-strategies/
├── src/
├── methodology.md
├── research-question.md
└── PROJECT_STATUS.md
````

## Reproducibility

The project is designed as a reproducible technology-intelligence workflow.

Search strategies, processing scripts, classification steps, validation procedures, analytical reports and figures are retained separately so that the development of the landscape can be inspected and updated.

Most analytical transformations are implemented in Python rather than through manual editing of derived datasets.

## Project status

The core scientific, patent and science–patent integration analyses have been completed.

A first complete version of the final technology landscape report is available here:

[Read the final PFAS Water Technology Landscape](reports/final-technology-landscape.md)

Further work may extend the landscape with additional patent technologies, commercial intelligence and ongoing monitoring.


