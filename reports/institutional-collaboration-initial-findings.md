# Initial Institutional Collaboration Analysis

## Method

Institutional collaboration was measured at the publication level.

Each unique pair of institutions appearing on the same publication was
counted once for that publication, regardless of the number of authors
from each organization.

The analysis uses the enriched OpenAlex authorship dataset containing:

- 658 publications
- 4,793 authorship–institution rows
- 1,067 normalized institutions
- 70 countries

Institutional aliases and confirmed affiliation-resolution errors were
corrected before collaboration counts were calculated.

The main corrections included:

- University of Campania duplicate OpenAlex records
- Albany State University records incorrectly assigned from University
  at Albany affiliations
- University of Washington Tacoma records incorrectly assigned from
  University of Washington and Aquagga affiliations
- Ghana Environmental Protection Agency records incorrectly assigned
  from explicit U.S. EPA affiliations

The analysis distinguishes:

- `external`: collaboration between separate organizations
- `parent_subunit`: known parent-organization and institute relationship
- `possible_internal`: likely university and internal-centre relationship

Parent–subunit and possible-internal pairs remain in the detailed CSV
output but are excluded from the printed headline ranking.

## Network coverage

The normalized collaboration network contains:

| Measure | Count |
|---|---:|
| Publications analyzed | 658 |
| Institution pairs | 3,525 |
| Institutions with at least one collaboration link | 1,019 |
| International country pairs | 388 |

These counts include publications from every analysis tier.

The principal interpretation should prioritize core publications and,
where appropriate, secondary and manually reviewed records.

## Strongest external institutional collaborations

| Institution A | Institution B | Core publications | Primary publications |
|---|---|---:|---:|
| U.S. Environmental Protection Agency | Ohio Environmental Protection Agency | 4 | 5 |
| Colorado School of Mines | Arizona State University | 4 | 5 |
| State Key Joint Laboratory of Environment Simulation and Pollution Control | Tsinghua University | 3 | 4 |
| University of Washington | Xi'an Jiaotong University | 3 | 4 |
| CDM Smith | Arizona State University | 3 | 3 |
| China University of Mining and Technology | Auburn University | 3 | 3 |
| Colorado School of Mines | CDM Smith | 3 | 3 |
| Norwegian Geotechnical Institute | Norwegian University of Science and Technology | 3 | 3 |
| State Key Laboratory of Pollution Control and Resource Reuse | Nanjing University | 3 | 3 |
| Swedish University of Agricultural Sciences | Vrije Universiteit Amsterdam | 3 | 3 |
| Universitat de Girona | Catalan Institute for Water Research | 3 | 3 |
| University of Maryland, Baltimore County | Auburn University | 3 | 3 |
| University of Technology Sydney | Wenzhou University | 3 | 3 |
| Arcadis UK | Riverside | 2 | 3 |
| CSIRO | Colorado State University | 2 | 3 |

## Initial interpretation of leading pairs

The U.S. EPA and Ohio EPA form one of the strongest repeated public-sector
links in the corpus.

Colorado School of Mines and Arizona State University show a sustained
research relationship across PFAS treatment topics, including ion
exchange, resin systems, life-cycle assessment and membrane concentrates.

University of Washington and Xi'an Jiaotong University form a coherent
international collaboration around hydrothermal and supercritical-water
PFAS destruction.

CDM Smith appears in repeated collaborations with both Arizona State
University and Colorado School of Mines, indicating a visible
industry–academia connection around applied PFAS treatment.

China University of Mining and Technology and Auburn University show
repeated collaboration in photocatalytic PFAS degradation.

The Girona–Catalan Institute for Water Research pair represents a
regional Spanish research cluster within the corpus.

## Institutions with the broadest core collaboration networks

| Institution | Country | Core partners | Core collaboration links |
|---|---|---:|---:|
| Swedish University of Agricultural Sciences | Sweden | 33 | 48 |
| U.S. Environmental Protection Agency | United States | 31 | 35 |
| ETH Zurich | Switzerland | 31 | 31 |
| Colorado School of Mines | United States | 29 | 36 |
| Chinese Academy of Sciences | China | 26 | 30 |
| Vrije Universiteit Amsterdam | Netherlands | 25 | 37 |
| Helmholtz Centre for Environmental Research | Germany | 25 | 36 |
| Jacobs | United States | 25 | 25 |
| University of Guelph | Canada | 25 | 25 |
| University of Copenhagen | Denmark | 24 | 35 |

The Swedish University of Agricultural Sciences has the broadest core
collaboration network in the corpus.

Its 33 core partners and 48 core collaboration links indicate that it is
not only a high-output institution but also a highly connected actor.

The U.S. EPA and Colorado School of Mines combine relatively high
publication output with broad collaboration networks.

ETH Zurich has 31 core partners and 31 links, suggesting a wide network
with relatively few repeated links to the same partners.

Vrije Universiteit Amsterdam, the Helmholtz Centre for Environmental
Research and the University of Copenhagen also show strong network
connectivity.

Applied organizations are visible among the main network hubs. Jacobs,
for example, has 25 core collaborators, indicating substantial
participation in multi-institutional PFAS research.

## Leading international country collaborations

| Country A | Country B | Core publications | Primary publications |
|---|---|---:|---:|
| China | United States | 19 | 31 |
| United Kingdom | United States | 9 | 15 |
| Australia | United States | 8 | 11 |
| Australia | China | 7 | 11 |
| India | United States | 7 | 9 |
| Canada | United States | 6 | 7 |
| Denmark | United States | 5 | 6 |
| Spain | United States | 5 | 5 |
| Australia | India | 4 | 6 |
| Norway | United States | 4 | 5 |

The China–United States axis is the largest international collaboration
route in the corpus by a substantial margin.

The United States is involved in seven of the ten strongest country
pairs, reinforcing its central position in the scientific network.

Australia also occupies an important international position, with strong
links to the United States, China, India and the United Kingdom.

Spain appears among the ten strongest country pairs through its
collaboration with the United States.

## Industry, government and applied-research participation

The network contains several visible connections between universities
and applied organizations.

Examples include:

- CDM Smith with Arizona State University
- CDM Smith with Colorado School of Mines
- Arcadis with the University of Surrey
- CSIRO with Colorado State University
- Luleå University of Technology with Eurostep
- U.S. EPA with Ohio EPA

These links suggest that parts of the scientific literature are already
connected to engineering practice, public-sector implementation and
commercial technology development.

The prominence of government environmental agencies is particularly
important because PFAS treatment research is strongly influenced by
regulatory requirements, drinking-water standards and remediation
programmes.

## Relationship-quality controls

Institutional collaboration data from OpenAlex should not be treated as
error-free.

The analysis identified three main quality problems:

1. Duplicate institution entities
2. Incorrect institution resolution from raw affiliation strings
3. Parent-organization and subunit relationships represented as separate
   institutions

Confirmed mapping errors were corrected using conservative rules based on
OpenAlex IDs and raw affiliation text.

Known parent–subunit and possible-internal relationships were retained in
the detailed output but excluded from the headline external-collaboration
ranking.

Examples include:

- Chinese Academy of Sciences and the Research Center for
  Eco-Environmental Sciences
- Aarhus University and the Aarhus University Centre for Water
  Technology

Some remaining pairs should be reviewed before publication-quality
network visualizations are produced. These include vaguely named or
potentially internal organizations such as `Riverside` and selected
state-key-laboratory records.

## Interpretation constraints

Co-authorship indicates a publication relationship, not necessarily a
formal strategic partnership.

Whole counting is used. A publication with several institutions creates
one link for every unique institutional pair.

Large multi-institution papers can therefore generate many network links.

Country collaboration counts also use whole counting. A multinational
publication contributes once to every country pair represented on the
paper.

The broadest-network ranking currently counts every core collaboration
link, including links associated with review articles and large
consortia.

Network position should therefore be interpreted alongside:

- publication volume
- technology specialization
- number of repeated collaborations
- institutional type
- analysis tier
- underlying publication titles

## Initial strategic implications

The institutional landscape is not dominated by a single organization.

Instead, it contains several overlapping clusters:

- U.S. applied-treatment and regulatory networks
- U.S.–China destructive-treatment collaborations
- Australian and Asian photocatalysis and treatment-material networks
- Nordic and European environmental-science networks
- public–private engineering partnerships

Colorado School of Mines, Arizona State University, the U.S. EPA and the
Swedish University of Agricultural Sciences appear especially important
because they combine publication activity with network connectivity.

The University of Washington–Xi'an Jiaotong University collaboration is
notable for its focus on hydrothermal and supercritical-water treatment.

CDM Smith's repeated links to Arizona State University and Colorado
School of Mines make it a strong candidate for later company-level
technology-intelligence analysis.

The next analytical stage should connect institution networks to:

1. technology specialization
2. publication growth
3. company participation
4. patent and commercial activity