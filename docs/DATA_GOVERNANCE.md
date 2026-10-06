---
title: Data Governance
description: How GRIMdata handles sources, interpretation, privacy and the research record.
---

# Data Governance

Good research needs a clear account of where evidence came from, how it was interpreted and what happens when it is shared. For GRIMdata, that also means asking who becomes more visible when information is collected, connected or published.

## Purpose {#purpose}

<span id="mission-alignment"></span>

The research examines documented conditions, rights and public decisions. Each inquiry starts with a question: what information is needed to understand this situation, and what detail serves that purpose?

An accessible document can become much more revealing when it is indexed or linked to other records. The value of a comparison needs to be considered alongside the exposure it creates.

## Methods and interpretation {#methods-and-interpretation}

<span id="cultural-sensitivity-research-stance"></span>
<span id="non-imposing-methodology"></span>
<span id="ethical-research-practices"></span>
<span id="1-do-no-harm"></span>
<span id="2-transparency"></span>
<span id="3-reproducibility"></span>
<span id="4-accountability"></span>
<span id="international-considerations"></span>
<span id="multi-jurisdictional-data"></span>
<span id="language-translation"></span>

Document selection, search terms, classifications and scoring rules are research choices. Record those choices, explain ambiguous cases and keep the source material distinguishable from the interpretation.

Legal and cultural context matters. Country-level comparisons sit alongside document-level evidence, source dates, language coverage and written assessments. Missing evidence stays visible as a gap.

[Research Context](RESEARCH_CONTEXT.md) develops these ideas; [Scorecard Design & Methodology](scorecard/design.md) explains the current indicators.

## Sources and attribution {#sources-and-attribution}

<span id="data-collection-principles"></span>
<span id="1-public-domain-documents-only"></span>
<span id="2-source-attribution"></span>
<span id="3-respect-for-terms-of-service"></span>

The DigitalChild pipeline works with publicly available human-rights and policy documents. Record the publisher, source URL, document date, access date and processing version where available. Keep the original reference when translating or normalizing material.

Source terms guide collection and reuse. Check the publisher's permissions, use an API or bulk download where available, and configure scraping requests for the source. [Metadata Schema](standards/METADATA_SCHEMA.md) describes the fields used to record provenance.

## People and privacy {#people-and-privacy}

<span id="privacy-data-protection"></span>
<span id="personal-information"></span>
<span id="data-storage"></span>
<span id="data-sharing"></span>
<span id="research-ethics"></span>
<span id="human-subjects"></span>
<span id="institutional-review-board-irb"></span>
<span id="publication-ethics"></span>
<span id="contributor-conduct"></span>
<span id="issue-reporting"></span>
<span id="user-expectations"></span>

Human-rights documents may identify survivors, defenders or other individuals. Search, extraction and aggregation can increase their exposure even when the original document was public.

Use the detail needed to answer the research question. Consider whether an aggregate, a source reference or restricted access would serve it better than publishing an identifiable extract. Pay particular attention to outing, selective enforcement and misclassification.

The public website provides research and exploration tools; it accepts no participant submissions.

## Storage and access {#storage-and-access}

<span id="security-access-control"></span>
<span id="data-access"></span>
<span id="security-measures"></span>
<span id="secure-deployment"></span>

Public browsing, documentation search and table filtering need no account. The site serves published research files; search and filtering happen in the browser. External charts load when you choose them. [Site practices](practices/index.md) explains those interactions and the information involved.

Researchers running DigitalChild locally manage their own files, access permissions, backups and retention. The self-hosted API includes authentication, rate limits and validation settings. [Production deployment guidance](guides/PRODUCTION_DEPLOYMENT.md) covers configuring that service.

## Quality and revisions {#quality-and-revisions}

<span id="data-quality-integrity"></span>
<span id="source-validation"></span>
<span id="metadata-integrity"></span>
<span id="error-handling"></span>
<span id="updates-versioning"></span>
<span id="data-updates"></span>
<span id="policy-updates"></span>

Review source availability, extraction quality, document dates and interpretation. Record retrieval failures and coverage gaps, and retain original values when normalization changes them. [Validation guidance](guides/VALIDATORS_USAGE.md) describes the available checks.

The published scorecard snapshot was generated on **26 June 2026**. Its metadata records source verification on **9 September 2025**. These dates identify the export and source-review stages respectively.

A revised assessment should record what changed, why and which source supports it. Keep the relevant version and date with published outputs so later work can be compared with the earlier record.

## Retention and corrections {#retention-and-corrections}

<span id="data-retention-deletion"></span>
<span id="default-retention"></span>
<span id="right-to-be-forgotten"></span>
<span id="community-standards"></span>

Retain research material for a defined purpose, taking account of source rights and the people represented in it. Revisit access and retention when the research question or use changes.

Corrections should explain the change without repeating sensitive material. Earlier versions may remain in repository history, archives and downloaded copies. [Repository terms](CONTRIBUTING.md) describes contribution attribution and licensing; public issue records are unsuitable for personal or confidential material.

## Publication and reuse {#publication-and-reuse}

<span id="compliance-legal"></span>
<span id="copyright"></span>
<span id="data-protection-laws"></span>
<span id="freedom-of-information"></span>
<span id="contact-questions"></span>
<span id="data-quality-issues"></span>
<span id="ethical-concerns"></span>
<span id="collaboration"></span>

| Material | Access and terms |
| --- | --- |
| DigitalChild source code | MIT, as specified in the repository licence |
| Project-authored DigitalChild data and documentation | CC BY 4.0 where specified; credit the work and its sources |
| Third-party documents | Original publisher and source terms |
| Published articles | Their respective publication terms |
| Historical HumanRights research archive | Private archive |
| Future project material | Terms will follow the sources, methods and people involved |

Cite the research or output version you used. The [technical overview](docs/technical-overview.md#citation) provides the software citation, and the [project pages](projects/index.md) link to the published studies.

[Research Context](RESEARCH_CONTEXT.md) · [Site practices](practices/index.md) · [Research directions](research-directions/index.md)
