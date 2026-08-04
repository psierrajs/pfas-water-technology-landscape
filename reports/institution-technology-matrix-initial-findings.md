# Initial Institution–Technology Matrix Analysis

## Purpose

This analysis maps institutions against PFAS water-treatment technologies.

The objective is to identify:

* organizations with broad technology coverage;
* institutions with repeated activity across several treatment areas;
* specialist institutions concentrated in a smaller number of technologies;
* apparently broad profiles created by a single multitechnology review or report.

## Method

The matrix was constructed from the enriched OpenAlex authorship dataset.

It contains:

* 4,793 authorship–institution rows;
* 517 normalized institutions;
* 12 technology columns.

Only publications in the following analysis tiers were included:

* `core`;
* `secondary`;
* `manual_review`.

Each matrix row represents one normalized institution.

Each technology column contains the number of unique publications assigned to that institution and technology.

A publication is counted once per institution and technology, regardless of the number of affiliated authors.

The same institutional alias and affiliation-correction rules used in the collaboration and momentum analyses were applied.

## Breadth metrics

Two measures of technology breadth are used.

### Active technology count

The number of technologies in which an institution has at least one publication.

This is useful for screening, but it can exaggerate breadth when a single review article receives several technology labels.

### Supported technology count

The number of technologies in which an institution has at least two publications.

This is the preferred measure for identifying credible multitechnology activity.

A technology supported by two or more publications is more likely to represent repeated institutional participation rather than a single broad review, consortium paper or affiliation artefact.

## Leading institutions by supported technology breadth

| Institution                                 | Country       | Supported technologies | Active technologies | Unique publications |
| ------------------------------------------- | ------------- | ---------------------: | ------------------: | ------------------: |
| U.S. Environmental Protection Agency        | United States |                      7 |                  11 |                  10 |
| Clarkson University                         | United States |                      5 |                   5 |                  11 |
| Colorado School of Mines                    | United States |                      4 |                   5 |                  12 |
| New Jersey Institute of Technology          | United States |                      3 |                   6 |                   7 |
| Ohio Environmental Protection Agency        | United States |                      3 |                   6 |                   4 |
| Swedish University of Agricultural Sciences | Sweden        |                      3 |                   5 |                   9 |
| Temple University                           | United States |                      3 |                   5 |                   6 |
| Arcadis US                                  | United States |                      3 |                   5 |                   4 |
| Arizona State University                    | United States |                      3 |                   4 |                   9 |
| Luleå University of Technology              | Sweden        |                      3 |                   4 |                   6 |
| Aarhus University                           | Denmark       |                      3 |                   3 |                   6 |
| Kyoto University                            | Japan         |                      3 |                   3 |                   4 |
| University of Southern Queensland           | Australia     |                      3 |                   3 |                   3 |

## Initial interpretation

The U.S. EPA has the broadest technology profile in the dataset.

It is active in 11 technologies, of which seven are supported by at least two publications.

Clarkson University has a particularly coherent multitechnology profile because all five of its active technologies are supported by repeated publications.

Its strongest areas are:

* plasma;
* electrochemical oxidation;
* sonolysis;
* ion exchange;
* adsorption.

Colorado School of Mines combines high publication volume with repeated activity across four technologies.

Its strongest areas are:

* adsorption;
* membranes;
* ion exchange;
* supercritical water oxidation.

Arizona State University has a more focused but strongly supported profile centred on:

* ion exchange;
* adsorption;
* photocatalysis.

Aarhus University shows repeated activity across hydrothermal treatment, adsorption and photocatalysis.

Luleå University of Technology combines electrochemical oxidation, adsorption and photocatalysis, with additional sonolysis activity.

The University of Georgia has fewer supported technologies, but its profile is strongly concentrated in electrochemical oxidation and ion exchange.

## Why supported breadth is necessary

Several institutions initially appeared highly multitechnology despite having only one or two publications.

Examples include organizations with five or six active technologies generated from a single broad review, report or consortium publication.

These cases demonstrate that active technology count alone is not a reliable indicator of institutional capability.

The supported technology count reduces this distortion by requiring repeated publication evidence.

It should therefore be used as the primary breadth indicator in later rankings and visualizations.

## Validation of the U.S. EPA breadth signal

The U.S. EPA initially appeared active across 11 technologies.

Inspection of the underlying publications shows that this breadth is partly genuine and partly influenced by broad multitechnology reviews.

Repeated publication support exists for:

* adsorption;
* ion exchange;
* membranes;
* thermal treatment;
* supercritical water oxidation;
* electrochemical oxidation;
* plasma;
* sonolysis.

The strongest repeated areas are adsorption, ion exchange and membranes, each represented by three publications.

Several additional technologies are supported by two publications.

However, two broad reviews contribute multiple labels at once:

* a 2022 review of thermal and nonthermal PFAS degradation contributes hydrothermal, plasma, sonolysis and thermal labels;
* a 2023 photocatalysis review contributes adsorption, ion exchange, membranes, photocatalysis and sonolysis labels.

The EPA should therefore be interpreted as a genuinely broad organization, but not as having 11 equally mature or independent technology programmes.

Its strongest role appears to combine:

* drinking-water treatment evaluation;
* regulatory and public-sector research;
* assessment of multiple destructive technologies;
* treatment of concentrated and residual PFAS streams;
* publication of broad state-of-the-field reviews.

## Specialist and focused profiles

The matrix also highlights institutions with narrower but more coherent specialization.

### Clarkson University

Clarkson University has five active technologies, all supported by repeated publication evidence.

Its profile is strongest in:

* plasma;
* electrochemical oxidation;
* sonolysis.

This makes Clarkson one of the clearest destructive-treatment specialists in the dataset.

### Colorado School of Mines

Colorado School of Mines combines the highest publication volume among the leading multitechnology institutions with four supported technologies.

Its profile is strongest in:

* adsorption;
* membranes;
* ion exchange;
* supercritical water oxidation.

This suggests a broad treatment portfolio spanning both capture and destruction.

### Arizona State University

Arizona State University shows a focused capture-oriented profile dominated by:

* ion exchange;
* adsorption;
* photocatalysis.

Its repeated collaboration with CDM Smith and Colorado School of Mines reinforces its relevance to applied treatment development.

### University of Georgia

The University of Georgia has only two supported technologies but a strong concentration in electrochemical oxidation.

Its publication sequence also demonstrates repeated integration with:

* ion exchange;
* foam fractionation;
* life-cycle assessment.

Its value lies more in process integration and capture-and-destroy development than in broad technology coverage.

### University of Surrey and Arcadis UK

The University of Surrey and Arcadis UK have focused profiles centred on sonolysis.

Their repeated joint publications make them more strategically significant than their total breadth scores alone would suggest.

This illustrates why the matrix should be interpreted together with the collaboration and momentum analyses.

## Low-volume breadth

A separate group contains institutions with five or more active technologies but fewer than three publications.

These cases are likely to be driven by:

* broad review articles;
* multitechnology reports;
* large consortium papers;
* incorrect or weak affiliation assignments;
* one publication receiving several technology labels.

Examples include:

* United States Department of Defense;
* United States Army Corps of Engineers;
* Strategic Environmental Research and Development Program;
* National Council for Science and the Environment;
* Alcoa;
* several Korean universities;
* several commercial organizations with only one associated publication.

These records should not be interpreted as evidence of broad institutional capability without manual validation.

## Strategic interpretation

The matrix suggests three distinct institutional archetypes.

### Broad multitechnology organizations

These organizations combine repeated activity across several treatment areas.

Examples include:

* U.S. EPA;
* Clarkson University;
* Colorado School of Mines;
* New Jersey Institute of Technology.

### Focused technology specialists

These organizations show repeated activity concentrated in one or two technologies.

Examples include:

* University of Georgia in electrochemical oxidation;
* University of Surrey and Arcadis UK in sonolysis;
* Rice University in photocatalysis;
* Battelle in supercritical water oxidation.

### Capture-and-destroy integrators

These institutions connect capture technologies with destructive processes.

Examples include:

* University of Georgia;
* Colorado School of Mines;
* Arizona State University;
* Rice University;
* University of Southern Queensland.

This group may be especially important commercially because full-scale PFAS treatment often requires concentration, separation and destruction rather than a single treatment step.

## Limitations

Technology labels are assigned at publication level and may be broad.

Review papers can activate several technology columns simultaneously.

The supported technology threshold of two publications is conservative relative to a single-paper count, but it remains a low threshold.

Institutional publication counts do not measure:

* patent ownership;
* commercial deployment;
* technology readiness;
* funding;
* citation impact;
* corresponding-author leadership;
* scale of experimental work.

The matrix also does not yet distinguish between:

* laboratory studies;
* pilot demonstrations;
* field demonstrations;
* reviews;
* life-cycle assessments;
* techno-economic studies.

## Recommended use

The matrix should be used as a screening tool rather than a final ranking of institutional capability.

The most reliable interpretation comes from combining:

* supported technology breadth;
* total publication volume;
* momentum over time;
* repeated collaboration links;
* underlying publication titles;
* evidence of field or pilot deployment.

## Recommended next steps

The next analytical stage should:

1. classify publications by evidence type, such as review, laboratory, pilot and field demonstration;
2. create a visual heatmap using supported publication counts;
3. identify institutions that combine breadth with recent momentum;
4. distinguish capture-only, destruction-only and combined-treatment institutional profiles;
5. connect leading institutions to patents, companies and commercial projects.

