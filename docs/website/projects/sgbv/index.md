---
title: SGBV-UPR — Published research and planned renewal
description: Exploratory computational and legal research on SGBV in SADC UPR records, published in 2022, with planned global renewal.
---

# SGBV-UPR Project

[← Research tracks](../../../projects/index.md){ .md-button }

## Sexual and Gender-Based Violence Analysis

**Published research · Planned renewal**

How do states recognise and respond to sexual and gender-based violence in the Universal Periodic Review? The SGBV-UPR study developed a computational approach to finding, organizing and comparing relevant passages, then examined those passages in their legal context.

[Read the published study](https://doi.org/10.47348/SLR/2022/i1a1){ .md-button .md-button--primary }

## About This Project

The inquiry took shape in 2019; computational exploration began in 2020. A conference presentation in 2021 preceded publication in *Stellenbosch Law Review* in 2022.

The study examined Southern African Development Community (SADC) member states across the UPR cycles available at the time. It investigated SGBV and violence or discrimination related to sexual orientation, gender identity and expression, and sex characteristics (SOGIESC).

[Research history](../../../research-history/index.md) traces the exploratory work and its development into [LittleRainbowRights](../littlerainbowrights/index.md), which expanded country and document-source coverage.

## Research Questions

- How are SGBV and SOGIESC-related concerns expressed in UPR records?
- Which language patterns identify material worth closer legal examination?
- How do those patterns change between review cycles and countries?
- What do the selected passages reveal about state responses and the gap between rights commitments and implementation?

## Methodology

### Data Collection

An automated retrieval workflow gathered publicly available UPR documents and organized them by country and review cycle. The computational analysis used Python's Natural Language Toolkit (NLTK), customized language patterns and report generation. Variation in file formats, wording and source access shaped the approach.

### Analysis Approach

The published method grouped variants of terms such as *women*, *violence*, *gender identity* and *same-sex*. Paragraph ranking combined keyword matches, giving additional weight to person-related and violence-related terms appearing together. The workflow produced five reports for each country and cycle:

| Report | What it brought into view |
| --- | --- |
| Identified keywords | Which selected terms appeared in the document |
| Keyword shortlist and occurrences | Matches and their relative ranking |
| Ranked passages | Expanded paragraphs for contextual examination |
| Passages in source order | Relevant discussion in its original sequence |
| Keyword totals | Frequencies for country and cycle comparisons |

The computational choices—term variants, grouping, selection and ranking—developed through examination of the documents. Legal analysis connected selected passages to the UPR process, legal instruments and country context. [Sections 2–3 of the article](https://doi.org/10.47348/SLR/2022/i1a1) describe the workflow and country analyses.

### Interpretation and limitations

Keyword frequencies describe language in the selected documents. They do not measure violence prevalence or establish whether a recommendation was implemented. Corpus coverage, term selection and extraction quality shape the comparisons; the original third-cycle coverage was incomplete.

An experimental positive/negative language classification was excluded from the published analysis because its wording did not behave consistently across countries and cycles. That decision is part of the methodological record (section 4.1).

## Key Findings

**Changing language across cycles.** The article reports an increasing share of gender-based-violence mentions in the selected corpus, alongside changing use of violence-against-women terminology. These patterns opened questions about how states describe violence and whether different terms refer to overlapping concerns (section 3.3).

**Categories change what becomes visible.** The grouping of trafficking with sexual violence reflected its context in the examined texts. The article discusses how another grouping could change the apparent balance between sexual and gender-based violence. Classification was an analytical decision with consequences for interpretation.

**Rerunning an inquiry matters.** The workflow made it easier to revise search terms, regenerate reports and extend an investigation. The article identifies the cost of reproducibility and error correction as a substantial benefit for teams with limited time and resources (section 4.1).

!!! quote "Documentation under constraint"
    “It is therefore vital for computational models to handle what data does exist and to streamline all formats of data when incidents are documented.”

    — Vollmer & Vollmer (2022), section 4.3. [Published article](https://doi.org/10.47348/SLR/2022/i1a1)

[Research Context](../../../RESEARCH_CONTEXT.md) connects these findings to documentation during instability and to the wider GRIMdata programme.

<span id="project-status"></span>

## Future Development

### Planned renewal

The next investigation will complete the original Cycle 3 coverage and extend Cycle 4 analysis across all UPR countries. It will revisit the source collection, extraction and comparison methods, using country batches to build global coverage.

[Renewal questions and stages](../../../research-directions/index.md#sgbv-upr-renewal)

## Data & Visualizations

### Current Access

The public record is the [2022 article](https://doi.org/10.47348/SLR/2022/i1a1), including its methods, examples, country analyses and tables. The historical HumanRights research archive remains private.

## Publications

Vollmer, D. T., & Vollmer, S. C. (2022). *Global perspectives of Africa: Harnessing the universal periodic review to process sexual and gender-based violence in SADC member states.* *Stellenbosch Law Review*, 33(1), 8–41. [DOI: 10.47348/SLR/2022/i1a1](https://doi.org/10.47348/SLR/2022/i1a1).

## Citing This Work

### For the Journal Article

```bibtex
@article{vollmer2022sgbv,
  title = {Global perspectives of Africa: Harnessing the universal periodic review to process sexual and gender-based violence in SADC member states},
  author = {Vollmer, DT and Vollmer, SC},
  journal = {Stellenbosch Law Review},
  volume = {33},
  number = {1},
  pages = {8--41},
  year = {2022},
  doi = {10.47348/SLR/2022/i1a1}
}
```

### Access and citation terms {#for-the-dataset}

The article and its cited sources retain their respective publication and reuse terms.

## Related Work

[LittleRainbowRights](../littlerainbowrights/index.md) · [Research history](../../../research-history/index.md) · [Research Context](../../../RESEARCH_CONTEXT.md)

## Data Governance

SGBV records can identify people at risk. The research examines institutional responses while limiting unnecessary exposure of survivors and other individuals. [Data Governance](../../../DATA_GOVERNANCE.md) explains how source selection, interpretation and publication address that responsibility.

<span id="sgbv-categories-analyzed"></span>
<span id="key-features"></span>
<span id="acknowledgments"></span>
<span id="__span-1-1"></span>
<span id="__codelineno-1-1"></span>
<span id="__span-1-2"></span>
<span id="__codelineno-1-2"></span>
<span id="__span-1-3"></span>
<span id="__codelineno-1-3"></span>
<span id="__span-1-4"></span>
<span id="__codelineno-1-4"></span>
<span id="__span-1-5"></span>
<span id="__codelineno-1-5"></span>
<span id="__span-0-1"></span>
<span id="__codelineno-0-1"></span>
<span id="__span-0-2"></span>
<span id="__codelineno-0-2"></span>
<span id="__span-0-3"></span>
<span id="__codelineno-0-3"></span>
<span id="immediate-updates-needed"></span>
<span id="long-term-enhancements"></span>
<span id="coming-soon"></span>
<span id="how-to-use-this-data"></span>
<span id="for-researchers"></span>
<span id="for-advocates"></span>
<span id="for-policy-makers"></span>
<span id="repository-code"></span>
<span id="__span-2-1"></span>
<span id="__codelineno-2-1"></span>
<span id="__span-2-2"></span>
<span id="__codelineno-2-2"></span>
<span id="__span-2-3"></span>
<span id="__codelineno-2-3"></span>
<span id="__span-2-4"></span>
<span id="__codelineno-2-4"></span>
<span id="__span-3-1"></span>
<span id="__codelineno-3-1"></span>
<span id="__span-3-2"></span>
<span id="__codelineno-3-2"></span>
<span id="__span-3-3"></span>
<span id="__codelineno-3-3"></span>
<span id="__span-3-4"></span>
<span id="__codelineno-3-4"></span>
<span id="__span-3-5"></span>
<span id="__codelineno-3-5"></span>
<span id="__span-3-6"></span>
<span id="__codelineno-3-6"></span>
<span id="__span-3-7"></span>
<span id="__codelineno-3-7"></span>
<span id="__span-4-1"></span>
<span id="__codelineno-4-1"></span>
<span id="__span-4-2"></span>
<span id="__codelineno-4-2"></span>
<span id="__span-4-3"></span>
<span id="__codelineno-4-3"></span>
<span id="__span-4-4"></span>
<span id="__codelineno-4-4"></span>
<span id="__span-4-5"></span>
<span id="__codelineno-4-5"></span>
<span id="__span-4-6"></span>
<span id="__codelineno-4-6"></span>
<span id="__span-4-7"></span>
<span id="__codelineno-4-7"></span>
<span id="__span-4-8"></span>
<span id="__codelineno-4-8"></span>
<span id="__span-4-9"></span>
<span id="__codelineno-4-9"></span>
<span id="__span-4-10"></span>
<span id="__codelineno-4-10"></span>
<span id="__span-4-11"></span>
<span id="__codelineno-4-11"></span>
<span id="integration-with-grimdata"></span>
<span id="contributing"></span>
<span id="support-contact"></span>
