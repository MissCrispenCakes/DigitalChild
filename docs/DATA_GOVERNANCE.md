---
title: Data Governance
description: Purpose, provenance, information vulnerability, access, retention and project-specific publication terms for GRIMdata research.
---

# Data Governance

This page explains research responsibilities and the scope of the public DigitalChild/LittleRainbowRights materials. [Site practices](practices/index.md) describes public browsing and chart interactions. Planned tracks require their own decisions before collecting or releasing material.

## Purpose

The research uses documentary evidence to examine rights and public decisions. Governance asks what is necessary to collect, how a representation was produced, who can use it, and what exposure publication could create.

Knowing more about a situation may help people act while making those described more vulnerable. Public accessibility does not make every aggregation, inference or republication appropriate.

## Cultural Sensitivity & Research Stance

### Non-Imposing Methodology

Separate description of laws and documents from analysis of enforcement mechanisms and evaluation of effects. Recognise legal and cultural context, language limitations and the perspectives embedded in classifications.

The research focuses on autonomy and vulnerable populations. That stance is explicit; numerical assessments are not value-free substitutes for legal interpretation or lived experience. [Research Context](RESEARCH_CONTEXT.md) explains the reasoning.

## Data Collection Principles

### 1. Publicly Available Documents {#1-public-domain-documents-only}

The public pipeline is designed around publicly available human-rights and policy documents. This website does not collect participant submissions. Original sources may still contain sensitive material or carry copyright and reuse restrictions.

Review source terms, authentication boundaries and the necessity of collection before adapting a scraper. Public access does not establish permission to bypass controls or redistribute the document.

### 2. Source Attribution

Retain the original source URL, publisher, relevant dates and processing/version context where available. Distinguish a collection date, a verification date and the period a source describes. [Metadata schema](standards/METADATA_SCHEMA.md) documents the technical fields.

### 3. Respect for Terms of Service

Collection operators should assess source terms and applicable requirements, avoid bypassing access controls, and limit requests appropriately. Scraper settings and source behaviour must be checked for the particular deployment; the existence of code is not proof of compliance in every use.

## Privacy & Data Protection

### Personal Information

Institutional records may mention survivors, defenders, officials or other individuals. Extracted text can preserve names even when no separate personal-data fields are created. Assess whether indexing, linking or disclosure increases exposure and whether less detail would answer the research question.

### Data Storage

Local pipeline and API deployments are operated by their users. They determine storage location, access permissions and security. The public website serves published static research assets; it does not upload a visitor's local research corpus.

### Data Sharing

Prefer the minimum necessary detail. Consider aggregation, purpose, access and likely downstream reuse. Some research material should remain restricted even where source documents are public.

## Ethical Research Practices

### 1. Do No Harm

Treat harm reduction as a responsibility, not a guarantee. Examine risks of outing, selective enforcement, misclassification and exposing individuals. Institutional accountability does not require unnecessary visibility of affected people.

### 2. Transparency

Explain selection rules, classifications, missingness and changes. Make consequential interface choices understandable where they occur, including optional external charts.

### 3. Reproducibility

Preserve versions, processing context and references where disclosure is appropriate. Reproducibility does not require publishing sensitive information or third-party material without suitable rights.

### 4. Accountability

Research interpretations can be contested and revised. Retain the distinction between source evidence and authored judgment, and document material changes to public assessments.

## Data Quality & Integrity

### Source Validation

A reachable URL is not proof of source accuracy, present-day legal status or correct interpretation. Checks of availability, extraction and substantive meaning are different.

The visualization snapshot was generated **26 June 2026**; its metadata records source verification on **9 September 2025**. Interpret each date according to its meaning.

### Metadata Integrity

Preserve original values where normalization changes them, document transformations and keep gaps visible. Missing evidence must not silently become zero or a negative finding.

### Error Handling

Record failed retrievals and extraction issues. A successful run does not establish a complete corpus. [Validation guidance](guides/VALIDATORS_USAGE.md) explains the available tools.

## International Considerations

### Multi-Jurisdictional Data

Interpretation and publication may have different consequences across jurisdictions. Legal and policy sources need contextual review; a common schema does not erase those differences.

### Language & Translation

Language coverage and translation affect retrieval and classification. Report language limits, preserve original references and validate translated interpretations where they matter.

## Security & Access Control

### Data Access

Public site browsing, documentation search and table filtering need no account. The self-hosted API is separate software; its operator controls authentication, rate limits and access.

### Security Measures

DigitalChild contains validation and API security facilities. Their effectiveness depends on configuration, deployment and maintenance. Do not treat a documented feature as assurance for an unreviewed installation.

### Secure Deployment

[Production deployment guidance](guides/PRODUCTION_DEPLOYMENT.md) covers the self-hosted service. The website does not imply that a public API service is deployed.

## Data Retention & Deletion

### Default Retention

Local research operators determine retention according to purpose, source rights and relevant obligations. Versioned public outputs can remain in Git history, archives and downloaded copies.

### Corrections and Removal Requests {#right-to-be-forgotten}

Correcting a future version does not guarantee removal from existing copies. Assess the need for a correction, restriction or removal without reproducing sensitive material in public records. Historical versions and their limitations should remain distinguishable from current assessments.

## Research Ethics

### Human Subjects

Public-document research can still involve identifiable people and sensitive content. Any future participant work needs appropriate scope, ethics review and understandable terms before collection.

### Institutional Review Board (IRB)

Researchers must assess institutional review requirements for their own questions and methods. No participant recruitment or consent process operates through this website.

### Publication Ethics

Cite the relevant study or output version, explain the method, retain limitations and observe source/publication terms. The [technical overview](docs/technical-overview.md#citation) provides the software citation.

<span id="contributor-conduct"></span>
<span id="issue-reporting"></span>
<span id="user-expectations"></span>

## Community Standards

Existing [contribution terms](CONTRIBUTING.md) describe attribution and licensing for repository material. A public versioned record may retain earlier contributions after later changes. Personal or confidential material does not belong in public issue histories.

## Compliance & Legal

### Copyright

| Material | Access and terms |
| --- | --- |
| DigitalChild source code | MIT, as specified in the repository licence |
| Project-authored DigitalChild data and documentation | CC BY 4.0 where specified; attribution required |
| Original third-party documents | Publisher/source terms remain applicable |
| Published articles and archival records | Their own publication terms; cite the actual work |
| Historical HumanRights research archive | Private; no public download or general open licence is offered here |
| Future project material | Access and release terms remain to be determined |

### Data Protection Laws

Public-document processing can create privacy and data-protection obligations. Deployment operators and researchers must assess applicable requirements, source terms and sensitive categories for their use.

### Freedom of Information

Access to a public record does not establish permission for every subsequent research use, inference or republication.

<span id="contact-questions"></span>
<span id="data-quality-issues"></span>
<span id="ethical-concerns"></span>
<span id="collaboration"></span>

## Updates & Versioning

### Data Updates

Published scorecard snapshots have dates and version context. Pipeline tools support processing, comparison and exports; they do not establish uninterrupted or real-time monitoring of every source.

### Policy Updates

Governance decisions should be revisited when sources, purposes, access arrangements or research methods change. Git history records revisions to these public documents.

## Mission Alignment

Inspectable evidence, contextual interpretation and proportionate disclosure support the programme's research purpose. The four tracks have different materials and stages of development; their governance practices must be assessed accordingly.

[Research Context](RESEARCH_CONTEXT.md) · [Site practices](practices/index.md) · [Research directions](research-directions/index.md)

*Reviewed: 5 October 2026.*
