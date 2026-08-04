# Initial Institution–Technology Momentum Analysis

## Purpose

This analysis identifies institutions that show increasing activity in specific PFAS water-treatment technologies.

The objective is not simply to rank organizations by publication volume. It is to distinguish:

* established institutions with increasing output;
* emerging entrants with no publications in the early period;
* sustained research programmes;
* potentially important science-to-application trajectories.

## Method

The analysis uses the enriched OpenAlex authorship dataset and links each institution to the technology labels assigned to its publications.

The dataset contains:

* 658 publications;
* 4,793 authorship–institution rows;
* 982 normalized institution–technology combinations after alias correction.

Only publications in the following analysis tiers were included:

* `core`;
* `secondary`;
* `manual_review`.

The time periods were defined as:

* early period: 2018–2021;
* recent period: 2022–2025.

The two periods contain four complete publication years each. Records from 2026 were excluded because the year is incomplete.

For each institution–technology combination, the analysis calculates:

* number of unique publications in the early period;
* number of unique publications in the recent period;
* absolute change between periods;
* ratio of recent to early publications;
* total primary-corpus publications.

Publications are counted once per institution and technology, regardless of the number of affiliated authors.

## Momentum categories

Two types of momentum are reported.

### Established momentum

An institution is classified as showing established momentum when:

* it has at least one publication in the early period; and
* its recent-period publication count is greater than its early-period count.

### Emerging entrant

An institution is classified as an emerging entrant when:

* it has no publications in the early period; and
* it has at least two publications in the recent period.

These categories should be treated as screening indicators rather than definitive measures of technological leadership.

Institution-level publication counts remain relatively small, so apparent growth can be sensitive to individual papers, review articles and affiliation-resolution errors.

## Data-quality controls

The same institutional normalization rules used in the broader collaboration analysis were applied.

These include corrections for:

* duplicate University of Campania entities;
* University at Albany records incorrectly assigned to Albany State University;
* University of Washington records incorrectly assigned to University of Washington Tacoma;
* explicit U.S. EPA affiliations incorrectly resolved to the Ghana Environmental Protection Agency;
* Aarhus University Centre for Water Technology records consolidated under Aarhus University.

The Aarhus correction reduced the number of institution–technology combinations from 983 to 982 and removed duplicate momentum signals for the university and its internal centre.

## Leading established momentum signals

| Institution                             | Country        | Technology                    | Early publications | Recent publications | Change |
| --------------------------------------- | -------------- | ----------------------------- | -----------------: | ------------------: | -----: |
| University of Surrey                    | United Kingdom | Sonolysis                     |                  1 |                   3 |     +2 |
| University of Georgia                   | United States  | Electrochemical oxidation     |                  1 |                   3 |     +2 |
| Rice University                         | United States  | Photocatalysis                |                  1 |                   3 |     +2 |
| Arcadis UK                              | United Kingdom | Sonolysis                     |                  1 |                   3 |     +2 |
| Colorado School of Mines                | United States  | Adsorption                    |                  2 |                   3 |     +1 |
| University of Washington                | United States  | Supercritical water oxidation |                  1 |                   2 |     +1 |
| University of Illinois Urbana-Champaign | United States  | Electrochemical oxidation     |                  1 |                   2 |     +1 |
| University of British Columbia          | Canada         | Ion exchange                  |                  1 |                   2 |     +1 |
| U.S. Environmental Protection Agency    | United States  | Adsorption                    |                  1 |                   2 |     +1 |
| U.S. Environmental Protection Agency    | United States  | Ion exchange                  |                  1 |                   2 |     +1 |
| Drexel University                       | United States  | Plasma                        |                  1 |                   2 |     +1 |

The strongest established momentum signals are concentrated in destructive and combined-treatment technologies.

The University of Surrey and Arcadis show parallel growth in sonolysis, while the University of Georgia shows growth in electrochemical oxidation and Rice University in photocatalysis.

Colorado School of Mines has the largest early-period base among the leading results, increasing from two to three adsorption publications.

The remaining signals are based on small counts and should be interpreted together with the underlying publication titles.

## Validated emerging and growth case studies

### Battelle: supercritical water oxidation

Battelle appears as an emerging entrant in supercritical water oxidation, with three recent core publications and no publications in the early period.

The underlying records are:

* 2023 — *Application of Supercritical Water Oxidation to Effectively Destroy Per- and Polyfluoroalkyl Substances in Aqueous Matrices*
* 2024 — *Field Demonstration of PFAS Destruction in Various Alcohol-Resistant AFFFs Using Supercritical Water Oxidation (SCWO)*
* 2025 — *PFAS destruction using supercritical water oxidation (SCWO) at Peterson Space Force Base*

This is a coherent technology signal rather than a classification artefact.

The sequence suggests progression from treatment of aqueous matrices toward field demonstrations and site-specific deployment.

Battelle should therefore be treated as a high-priority organization for later company and technology-intelligence analysis of PFAS destruction.

### University of Surrey and Arcadis: sonolysis

The University of Surrey and Arcadis show a sustained collaboration around ultrasonic PFAS destruction.

Their shared publications include:

* 2020 — *Ultrasonic degradation of perfluorooctane sulfonic acid (PFOS) correlated with sonochemical and sonoluminescence characterisation*
* 2022 — *Sonolysis of per- and poly fluoroalkyl substances (PFAS): A meta-analysis*
* 2023 — *Flow and temporal effects on the sonolytic defluorination of perfluorooctane sulfonic acid*
* 2024 — *Increasing efficiency and treatment volumes for sonolysis of per- and poly-fluorinated substances, applied to aqueous film-forming foam*

Arcadis also appears on a broader 2018 review of emerging PFAS-remediation technologies.

The joint sequence is significant because it moves from process characterization and synthesis of existing evidence toward operational variables, higher treatment efficiency and larger treatment volumes.

The 2024 AFFF study is the clearest indication of movement toward more applied treatment conditions.

Two of the shared records are classified as `manual_review`, so this signal should be presented with appropriate caution. Nevertheless, the repeated co-authorship and technical progression support the interpretation of a sustained industry–academia programme.

### University of Georgia: electrochemical oxidation and combined treatment

The University of Georgia shows increasing activity in electrochemical oxidation, with one publication in the early period and three in the recent period.

The associated publications are:

* 2021 — *Field demonstration of coupling ion-exchange resin with electrochemical oxidation for enhanced treatment of per- and polyfluoroalkyl substances (PFAS) in groundwater*
* 2022 — *Environmental Life Cycle Assessment (LCA) of Treating PFASs with Ion Exchange and Electrochemical Oxidation Technology*
* 2023 — *Foam fractionation and electrochemical oxidation for the treatment of per- and polyfluoroalkyl substances (PFAS) in environmental water samples*
* 2025 — *A review on the recent mechanisms investigation of PFAS electrochemical oxidation degradation: mechanisms, DFT calculation, and pathways*

This signal is best interpreted as a combined-treatment programme centred on electrochemical oxidation.

The work spans:

* field demonstration;
* integration with ion exchange;
* integration with foam fractionation;
* environmental life-cycle assessment;
* mechanistic synthesis.

The 2021–2023 sequence provides the strongest evidence of applied development. The 2025 review supports the breadth of institutional activity but should not be treated as direct evidence of a new experimental advance.

The University of Georgia is therefore relevant to the project’s `capture_and_destroy` theme as well as to electrochemical oxidation.

### Rice University: photocatalysis and integrated capture–destruction materials

Rice University shows growth from one early-period photocatalysis publication to three recent-period publications.

The associated records are:

* 2020 — *Efficient Photocatalytic PFOA Degradation over Boron Nitride*
* 2022 — *Titanium oxide improves boron nitride photocatalytic degradation of perfluorooctanoic acid*
* 2023 — *An Ultraviolet/Boron Nitride Photocatalytic Process Efficiently Degrades Poly-/Perfluoroalkyl Substances in Complex Water Matrices*
* 2024 — *Size-selective trapping and photocatalytic degradation of PFOA in Fe-modified zeolite frameworks*

The sequence shows a coherent materials-development trajectory:

* initial proof of concept using boron nitride;
* catalyst improvement through titanium oxide;
* testing in more complex water matrices;
* integration of selective trapping with photocatalytic degradation.

The 2024 study is especially relevant because it combines capture and destruction within a material architecture.

The 2022 record is classified as `manual_review`, but the overall programme remains a credible momentum signal.

## Other emerging entrants

Several additional institution–technology combinations appear as emerging entrants with at least three recent publications and no early-period publications.

These include:

| Institution                       | Country       | Technology                | Recent publications |
| --------------------------------- | ------------- | ------------------------- | ------------------: |
| University of Southern Queensland | Australia     | Adsorption                |                   3 |
| University at Albany, SUNY        | United States | Adsorption                |                   3 |
| Luleå University of Technology    | Sweden        | Adsorption                |                   3 |
| Luleå University of Technology    | Sweden        | Electrochemical oxidation |                   3 |
| Kyoto University                  | Japan         | Adsorption                |                   3 |
| Harbin Institute of Technology    | China         | Membranes                 |                   3 |
| Chongqing University              | China         | Membranes                 |                   3 |
| Chinese Academy of Sciences       | China         | Adsorption                |                   3 |
| CNRS                              | France        | Adsorption                |                   3 |
| Aarhus University                 | Denmark       | Adsorption                |                   3 |
| Aarhus University                 | Denmark       | Hydrothermal treatment    |                   3 |

These signals have not yet been validated against their underlying publication titles.

They should therefore be treated as candidates for follow-up screening rather than confirmed emerging programmes.

The `Riverside` sonolysis result also requires institutional-identity review before interpretation because the organization name is insufficiently specific.

## Interpretation

The momentum analysis indicates that several of the most interesting developments occur at the intersection of capture and destruction.

Examples include:

* ion exchange followed by electrochemical oxidation;
* foam fractionation followed by electrochemical oxidation;
* selective adsorption combined with photocatalytic degradation;
* field treatment of concentrated AFFF matrices using SCWO;
* sonolysis development focused on improved efficiency and treatment volume.

This supports the project’s decision to treat combined-treatment systems as a distinct analytical category rather than forcing every publication into capture-only or destruction-only groups.

The analysis also shows that raw publication growth is not sufficient on its own.

The most useful signals emerged only after inspecting:

* publication titles;
* analysis tiers;
* continuity over time;
* co-authorship relationships;
* movement from proof of concept toward field or process application.

## Limitations

The results are based on publication counts rather than citation-weighted impact, funding, patents or commercial deployment.

Institution-level counts are small, and growth ratios can be exaggerated when the early-period baseline is one publication.

Review articles are included in the primary corpus and can increase apparent activity without representing new experimental development.

Technology labels are assigned at publication level. A paper may therefore contribute to more than one institution–technology combination and more than one technology category.

OpenAlex affiliation mappings remain imperfect despite the corrections already applied.

The current analysis does not distinguish corresponding-author leadership from participation as a collaborating institution.

## Initial strategic implications

Four signals currently stand out as especially valuable for the broader landscape:

1. Battelle in supercritical water oxidation
2. University of Surrey and Arcadis in sonolysis
3. University of Georgia in electrochemical capture-and-destroy systems
4. Rice University in photocatalytic and integrated capture–destruction materials

Battelle is the clearest emerging applied-destruction actor identified so far.

The Surrey–Arcadis relationship is the clearest sustained industry–academia collaboration within a single destructive-treatment technology.

The University of Georgia provides one of the strongest examples of process integration and applied evaluation.

Rice University provides a strong example of materials innovation progressing toward integrated capture and degradation.

These organizations should be prioritized in later analyses of:

* patents;
* commercial partnerships;
* funded projects;
* field demonstrations;
* technology readiness;
* company positioning.

## Recommended next steps

The next stage should:

1. validate the remaining high-ranked emerging entrants;
2. classify institutions by organization type;
3. identify corresponding-author and repeated-team leadership;
4. connect momentum signals to patent assignees and companies;
5. produce a visual institution–technology matrix;
6. distinguish review-led activity from experimental and field-development activity.
