# Initial Evidence–Technology Matrix Analysis

## Purpose

This analysis links PFAS water-treatment technologies to the type of evidence available for each technology.

The objective is to identify which technologies have:

* explicit field-demonstration evidence;
* pilot-scale evidence;
* life-cycle assessment;
* clearly experimental publications;
* computational or mechanistic studies;
* predominantly review-level evidence;
* large evidence gaps under the current conservative classifier.

The matrix is intended to support later assessment of technology maturity and commercialization potential.

## Input data

The analysis uses:

`data/processed/evidence_type/openalex_evidence_type_classified.csv`

This dataset contains 449 publications from the primary analysis tiers:

* `core`;
* `secondary`;
* `manual_review`.

Each publication already contains:

* one or more technology labels;
* a primary evidence type;
* secondary evidence signals;
* an analysis tier.

The matrix counts unique publications by technology and primary evidence type.

A publication can contribute to more than one technology when it has multiple technology labels.

## Technologies included

The matrix contains 12 technology categories:

* adsorption;
* ion exchange;
* membranes;
* electrochemical oxidation;
* photocatalysis;
* plasma;
* sonolysis;
* supercritical water oxidation;
* hydrothermal treatment;
* thermal treatment;
* biological treatment;
* capture and destroy.

## Evidence categories included

The matrix uses the following primary evidence types:

* `field_demonstration`;
* `pilot`;
* `life_cycle_assessment`;
* `computational`;
* `mechanistic`;
* `experimental`;
* `review`;
* `other`.

The `techno_economic` and `laboratory` categories were omitted from the printed summary because the conservative title-based classifier assigned zero publications to both.

## Evidence maturity by technology

| Technology                    | Field | Pilot | LCA | Experimental | Computational | Mechanistic | Review | Total |
| ----------------------------- | ----: | ----: | --: | -----------: | ------------: | ----------: | -----: | ----: |
| Adsorption                    |     1 |     3 |   2 |            7 |             1 |           1 |     31 |   144 |
| Ion exchange                  |     1 |     2 |   2 |            0 |             0 |           0 |     11 |    50 |
| Electrochemical oxidation     |     1 |     2 |   1 |            5 |             1 |           1 |     10 |    57 |
| Supercritical water oxidation |     1 |     0 |   0 |            4 |             1 |           0 |      1 |    19 |
| Plasma                        |     0 |     1 |   0 |            4 |             0 |           0 |     10 |    38 |
| Photocatalysis                |     0 |     0 |   0 |           13 |             0 |           1 |     14 |    55 |
| Membranes                     |     0 |     0 |   0 |            0 |             0 |           0 |     13 |    41 |
| Sonolysis                     |     0 |     0 |   0 |            0 |             2 |           0 |      7 |    28 |
| Biological                    |     0 |     0 |   0 |            0 |             1 |           0 |      8 |    20 |
| Thermal                       |     0 |     0 |   0 |            0 |             1 |           0 |      5 |    19 |
| Hydrothermal                  |     0 |     0 |   0 |            0 |             0 |           0 |      4 |    18 |
| Capture and destroy           |     0 |     0 |   0 |            0 |             0 |           0 |      0 |     2 |

## Technologies with confirmed pilot or field evidence

Five technologies have explicit pilot or field evidence:

| Technology                    | Field demonstrations | Pilot studies | Total publications |
| ----------------------------- | -------------------: | ------------: | -----------------: |
| Adsorption                    |                    1 |             3 |                144 |
| Ion exchange                  |                    1 |             2 |                 50 |
| Electrochemical oxidation     |                    1 |             2 |                 57 |
| Supercritical water oxidation |                    1 |             0 |                 19 |
| Plasma                        |                    0 |             1 |                 38 |

These technologies currently provide the strongest title-level evidence of progression beyond conventional laboratory research.

## Initial interpretation

### Adsorption

Adsorption has the broadest and most mature evidence base in the corpus.

It combines:

* one field demonstration;
* three pilot studies;
* two life-cycle assessments;
* seven explicitly experimental publications;
* the largest total publication volume.

Its maturity profile is consistent with adsorption being one of the most established PFAS treatment approaches.

However, the large number of review publications also indicates that the field contains substantial synthesis and technology-comparison activity.

### Ion exchange

Ion exchange has a strong applied-evidence profile despite lower publication volume than adsorption.

It includes:

* one field demonstration;
* two pilot studies;
* two life-cycle assessments.

The absence of explicitly experimental titles should not be interpreted as an absence of experimental work.

Instead, many ion-exchange studies use titles focused on treatment performance, resin regeneration or drinking-water application without matching the conservative experimental patterns.

### Electrochemical oxidation

Electrochemical oxidation has one of the most balanced maturity profiles.

It combines:

* one field demonstration;
* two pilot studies;
* one life-cycle assessment;
* five explicitly experimental studies;
* computational and mechanistic evidence.

This suggests that electrochemical oxidation is being examined across multiple stages, from mechanism and reactor performance to integrated treatment and field application.

### Supercritical water oxidation

Supercritical water oxidation has a particularly strong maturity signal relative to its publication volume.

Among only 19 publications, it includes:

* one field demonstration;
* four explicitly experimental studies;
* one computational study;
* only one review.

This profile suggests a comparatively application-oriented literature rather than a field dominated by reviews.

The Battelle field-demonstration sequence identified in the institution-momentum analysis reinforces this interpretation.

### Plasma

Plasma has one pilot-scale publication and four explicitly experimental studies.

Its evidence base remains smaller and more review-heavy than adsorption or electrochemical oxidation, but the presence of pilot-scale work indicates progress beyond proof of concept.

### Photocatalysis

Photocatalysis has the largest explicit experimental count in the matrix, with 13 publications.

However, it has no title-level pilot or field evidence.

This suggests a strong laboratory and materials-development base but weaker evidence of scale-up or deployment.

Photocatalysis may therefore represent a scientifically active but less mature treatment route under the current evidence framework.

## Technologies without confirmed pilot or field evidence

Seven technologies do not currently have title-level pilot or field evidence in the matrix:

* photocatalysis;
* membranes;
* sonolysis;
* biological treatment;
* thermal treatment;
* hydrothermal treatment;
* capture and destroy.

This should not be interpreted as proof that no pilot or field work exists.

The current classifier only assigns a high-maturity category when the title contains explicit terms such as:

* `field demonstration`;
* `full-scale`;
* `pilot-scale`;
* `pilot treatment`;
* `pilot plant`.

Relevant studies can therefore remain in `other` when their titles describe treatment systems without naming the scale directly.

### Membranes

Membranes have 41 publications and 13 reviews but no explicit experimental, pilot or field classification.

This is likely an artefact of the conservative title rules rather than a true evidence gap.

Several membrane publications identified elsewhere in the project describe:

* high-pressure filtration;
* nanofiltration;
* reverse osmosis;
* membrane concentrates;
* real-water treatment.

A manual evidence review is therefore required before interpreting membrane maturity.

### Sonolysis

Sonolysis has 28 publications, including two computational studies and seven reviews.

The absence of pilot or field labels conflicts with the previously validated Surrey–Arcadis progression toward increased treatment volume and AFFF application.

This again shows that the automated evidence classifier captures only explicit scale terminology.

The 2024 Surrey–Arcadis study should be reviewed manually as a possible scale-up or pre-pilot signal.

### Hydrothermal treatment

Hydrothermal treatment has 18 publications and four reviews but no title-level experimental, pilot or field evidence.

This category may be affected by overlap with supercritical water oxidation and broader thermal labels.

A separate review of hydrothermal alkaline treatment, hydrothermal liquefaction and SCWO terminology is needed before drawing maturity conclusions.

### Capture and destroy

Only two publications are explicitly labelled `capture_and_destroy`.

Neither has a title-level evidence category.

This does not reflect the true volume of combined-treatment work because many relevant publications also carry separate labels such as:

* adsorption;
* ion exchange;
* foam fractionation;
* electrochemical oxidation;
* photocatalysis.

The capture-and-destroy taxonomy should therefore be refined before it is used for maturity ranking.

## Evidence profile archetypes

The matrix suggests several distinct technology profiles.

### Established capture technologies

Adsorption and ion exchange have the strongest evidence of deployment, pilot evaluation and life-cycle assessment.

Their profiles indicate relatively mature treatment routes with substantial practical evaluation.

### Emerging destructive technologies with application signals

Electrochemical oxidation, SCWO and plasma show explicit evidence of scale progression.

Electrochemical oxidation has the broadest evidence mix.

SCWO has the strongest application-oriented profile relative to its total publication volume.

Plasma has pilot evidence but a smaller and more review-heavy literature.

### Experimentally active but scale-limited technologies

Photocatalysis has extensive explicit experimental evidence but no confirmed pilot or field records.

This suggests strong scientific activity without equivalent evidence of deployment.

### Technologies requiring manual maturity review

Membranes, sonolysis, hydrothermal, biological and thermal treatment cannot be assessed reliably from the current automatic primary labels alone.

Their publications require title and abstract review, and in some cases inspection of the full paper.

## Methodological cautions

The matrix uses whole publication counting.

A publication with multiple technology labels contributes once to every matching technology.

The total number of publications across technologies therefore exceeds the number of unique publications in the classified corpus.

The primary evidence category is title based.

This improves precision but reduces recall.

The matrix does not yet account for:

* corresponding-author leadership;
* study scale reported only in the abstract;
* real-water versus synthetic-water experiments;
* laboratory versus bench-scale distinctions;
* technology readiness levels;
* commercial deployment not represented in academic literature;
* patents, funded projects or company announcements.

Review counts should not be treated as maturity evidence.

A large review literature can indicate scientific attention, uncertainty, fragmentation or active technology comparison rather than readiness for deployment.

## Strategic implications

The strongest confirmed maturity signals are concentrated in five technologies:

1. adsorption;
2. ion exchange;
3. electrochemical oxidation;
4. supercritical water oxidation;
5. plasma.

Among these, adsorption and ion exchange appear most established.

Electrochemical oxidation is notable because it spans mechanism, experiment, pilot, field and life-cycle evidence.

SCWO is notable because a relatively small literature contains field and experimental evidence with limited review dominance.

Photocatalysis appears scientifically dynamic but less mature in terms of explicit scale-up.

The matrix supports the broader conclusion that combined treatment systems are strategically important.

Several of the field and pilot records combine capture and destruction rather than relying on a single process.

## Recommended next steps

The next stage should:

1. manually validate every pilot and field record;
2. inspect high-value `other` records for hidden scale information;
3. calculate maturity indicators that normalize by total publication volume;
4. identify institutions and companies linked to high-maturity evidence;
5. distinguish review, original research and field evidence in momentum analysis;
6. create a heatmap of technology versus evidence type;
7. integrate the evidence matrix with patent and commercial data.


