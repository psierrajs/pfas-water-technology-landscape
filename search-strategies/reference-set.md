# Scientific Literature Reference Set

## Purpose

This reference set contains a small group of known relevant publications used to test whether the OpenAlex search strategy retrieves important PFAS water-treatment studies across different technology categories.

The reference set is not intended to be exhaustive or statistically representative.

## Initial publications

### Review and landscape publications

1. Occurrence of per- and polyfluoroalkyl substances (PFAS) in source water and their treatment in drinking water  
   Year: 2019  
   DOI: https://doi.org/10.1080/10643389.2019.1614848  
   Category: review / occurrence and treatment

2. Updated review on emerging technologies for PFAS contaminated water treatment  
   Year: 2022  
   DOI: https://doi.org/10.1016/j.cherd.2022.04.009  
   Category: technology review

3. Water Treatment Technologies for PFAS: The Next Generation  
   Year: 2018  
   DOI: https://doi.org/10.1111/gwmr.12281  
   Category: technology review

4. A review of PFAS remediation: Separation and degradation technologies for water and wastewater treatment  
   Year: 2025  
   DOI: https://doi.org/10.1016/j.jwpe.2025.107793  
   Category: technology review

### Adsorption and ion exchange

5. Removal of poly- and perfluoroalkyl substances (PFAS) from water by adsorption: Role of PFAS chain length, effect of organic matter and challenges in adsorbent regeneration  
   Year: 2019  
   DOI: https://doi.org/10.1016/j.watres.2019.115381  
   Category: adsorption

6. Sorptive removal of short-chain perfluoroalkyl substances (PFAS) during drinking water treatment using activated carbon and anion exchanger  
   Year: 2023  
   DOI: https://doi.org/10.1186/s12302-023-00716-5  
   Category: adsorption / ion exchange

### Destructive technologies

7. Breakdown Products from Perfluorinated Alkyl Substances (PFAS) Degradation in a Plasma-Based Water Treatment Process  
   Year: 2019  
   DOI: https://doi.org/10.1021/acs.est.8b07031  
   Category: plasma treatment

8. Electrochemical Oxidation for Treatment of PFAS in Contaminated Water and Fractionated Foam—A Pilot-Scale Study  
   Year: 2023  
   DOI: https://doi.org/10.1021/acsestwater.2c00660  
   Category: electrochemical oxidation / pilot scale

### Membrane technologies

9. High-pressure membrane filtration processes for separation of per- and polyfluoroalkyl substances (PFAS)  
   Authors: Tae Lee, Thomas F. Speth and Mallikarjuna N. Nadagouda  
   Year: 2022  
   DOI: https://doi.org/10.1016/j.cej.2021.134023  
   Category: membrane separation / nanofiltration / reverse osmosis  
   Discovery method: independent OpenAlex search using `PFAS membrane water treatment`

### Photocatalysis

10. Degradation of per- and polyfluoroalkyl substances (PFAS) in wastewater effluents by photocatalysis for water reuse  
    Authors: Chunjie Xia, Xian Lim, Haoran Yang, Boyd M. Goodson and Jia Liu  
    Year: 2022  
    DOI: https://doi.org/10.1016/j.jwpe.2021.102556  
    Category: photocatalytic degradation / wastewater reuse  
    Discovery method: independent OpenAlex search using `PFAS photocatalysis water degradation`

### Sonolysis

11. Ultrasonic degradation of perfluorooctane sulfonic acid (PFOS) correlated with sonochemical and sonoluminescence characterisation  
    Authors: Richard James Wood, Tim Sidnell, Ian Ross, Jeffrey McDonough, Judy Lee and Madeleine J. Bussemaker  
    Year: 2020  
    DOI: https://doi.org/10.1016/j.ultsonch.2020.105196  
    Category: sonolysis / ultrasonic degradation  
    Discovery method: independent OpenAlex search using `PFAS sonolysis water degradation`

### Supercritical water oxidation

12. Supercritical Water Oxidation as an Innovative Technology for PFAS Destruction  
    Authors: Max J. Krause, Eben Thoma, Endalkachew Sahle-Damesessie, Brian C. Crone, Andrew Whitehill, Erin Shields and Brian Gullett  
    Year: 2022  
    DOI: https://doi.org/10.1061/(ASCE)EE.1943-7870.0001957  
    Category: supercritical water oxidation / PFAS destruction  
    Discovery method: independent OpenAlex search using `PFAS supercritical water oxidation`

### Hydrothermal liquefaction

13. PFAS destruction through catalyzed hydrothermal liquefaction using modified hydrochar  
    Authors: Shukla Neha, Maja Nguyen, et al.  
    Year: 2025  
    DOI: https://doi.org/10.1016/j.jwpe.2025.107606  
    Category: catalyzed hydrothermal liquefaction / PFAS destruction  
    Discovery method: independent OpenAlex search using `PFAS hydrothermal liquefaction`

### Combined adsorption and electrochemical oxidation

14. Comparison of perfluorooctane sulfonate (PFOS), perfluorooctanoic acid (PFOA) and perfluorobutane sulfonate (PFBS) removal in a combined adsorption and electrochemical oxidation process  
    Authors: Antoine P. Trzcinski and Kouji H. Harada  
    Year: 2024  
    DOI: https://doi.org/10.1016/j.scitotenv.2024.172184  
    Category: combined adsorption and electrochemical oxidation / capture-and-destroy  
    Discovery method: independent OpenAlex search using `PFAS combined adsorption electrochemical oxidation`

## Initial recall test

The first OpenAlex query retrieved all eight publications initially listed in this reference set within its first ten results.

This is encouraging but does not demonstrate strong independent recall because those records were mainly discovered through the same query being evaluated.

Two additional publications were therefore identified through technology-specific searches:

* one membrane-filtration publication;
* one photocatalysis publication.

These independently discovered records were then tested against the general query `PFAS water treatment`.

### Recall-test result for the membrane reference

The general OpenAlex query `PFAS water treatment` retrieved the membrane-filtration publication at position 64.

This indicates that the broad query captures the publication, but ranks it substantially lower than the initial review, adsorption, plasma and electrochemical-oxidation records.

The result supports using larger retrieval sets for recall testing and technology-specific searches for underrepresented categories.

### Recall-test result for the photocatalysis reference

The photocatalysis publication is indexed in OpenAlex and was retrieved at position 113 for the general query `PFAS water treatment`.

This indicates that the broad query captures the publication, but ranks it substantially lower than the initial review, adsorption, plasma, electrochemical-oxidation and membrane records.

The result confirms that inspecting only the first 100 records would underestimate recall for some technology categories.

It also supports using:

* larger retrieval sets for recall testing;
* DOI-based validation against a reference set;
* technology-specific searches for underrepresented categories.

### Recall-test result for the sonolysis reference

The sonolysis publication is indexed in OpenAlex.

It was not retrieved within the first 500 results of the general query `PFAS water treatment`.

However, it was retrieved at position 8 for the technology-specific query `PFAS sonolysis water degradation`.

This indicates that the general query does not provide adequate practical recall for this technology category, even though the publication is indexed and easily retrieved using targeted terminology.

The result supports a combined search design consisting of:

* one broad cross-technology query;
* separate technology-specific queries;
* DOI-based validation against an independent reference set;
* deduplication of records retrieved through multiple searches.

### Recall-test result for the supercritical water oxidation reference

The publication is indexed in OpenAlex.

It was retrieved at position 52 for the broad query `PFAS water treatment`.

It was retrieved at position 1 for the technology-specific query `PFAS supercritical water oxidation`.

An initial false-negative result was caused by case-sensitive DOI comparison in the recall-testing script. OpenAlex returned the DOI in lowercase, while the reference DOI contained uppercase characters.

The DOI-normalisation function was updated to compare lowercase canonical DOI URLs.

### Recall-test result for the hydrothermal liquefaction reference

The publication is indexed in OpenAlex.

It was not retrieved within the first 500 results of the broad query `PFAS water treatment`.

It was retrieved at position 3 for the technology-specific query `PFAS hydrothermal liquefaction`.

This result provides further evidence that hydrothermal destruction technologies require targeted terminology in the literature search strategy.

### Recall-test result for the combined capture-and-destroy reference

The publication is indexed in OpenAlex.

It was not retrieved within the first 500 results of the broad query `PFAS water treatment`.

It was retrieved at position 28 for the technology-specific query `PFAS combined adsorption electrochemical oxidation`.

This result confirms that combined capture-and-destroy processes are poorly represented by the broad query and require targeted search terminology.

The position of 28 also suggests that alternative formulations may improve ranking, particularly queries using the exact process names rather than the broader term `PFAS`.

## Current recall-test interpretation

The general query retrieved ten of the eleven publications currently included in the reference set within the inspected result windows.

However, ranking varied substantially:

* the original eight records appeared within the first ten results;
* the membrane reference appeared at position 64;
* the photocatalysis reference appeared at position 113.
* the sonolysis reference was not found within the first 500 general-query results but appeared at position 8 in the technology-specific search.

The current evidence suggests that the query has promising recall for the tested publications, but ranking bias may make some technology categories less visible in small result samples.

Further independent references are still needed for:

* sonolysis;
* supercritical water oxidation;
* hydrothermal treatment;
* catalytic degradation;
* combined capture-and-destruction processes.
