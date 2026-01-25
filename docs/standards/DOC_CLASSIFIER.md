# Document Type Classifier

## Overview

The document type classifier automatically categorizes documents based on filename patterns, content keywords, and source metadata. This eliminates manual classification and ensures consistent categorization across the pipeline.

## Supported Document Types

The classifier supports 10 document types:

### 1. **Law**
Legislation, acts, statutes, regulations, legal frameworks

**Patterns**: act, law, legislation, statute, regulation, amendment, bill, code
**Content**: "enacted by parliament", "legislative act", "sections of this act"
**Priority**: 90/100

### 2. **Treaty**
International treaties, conventions, charters, protocols

**Patterns**: treaty, convention, charter, protocol, agreement, covenant
**Content**: "state parties", "ratification", "signatory"
**Priority**: 95/100

### 3. **TreatyBodyReport**
Reports from UN treaty bodies (OHCHR, CRC, CESCR, CCPR, etc.)

**Patterns**: ohchr, crc, cescr, ccpr, cedaw, cat, crpd, acerwc, achpr
**Content**: "treaty body", "concluding observations", "committee on"
**Priority**: 100/100

### 4. **UPR**
Universal Periodic Review documents

**Patterns**: upr, universal_periodic_review
**Content**: "universal periodic review", "working group on the upr"
**Priority**: 100/100

### 5. **Policy**
Government policies, strategies, frameworks, action plans

**Patterns**: policy, strategy, framework, action_plan, compact, agenda, roadmap
**Content**: "policy framework", "strategic plan", "national strategy"
**Priority**: 60/100

### 6. **Guidelines**
Best practices, recommendations, operational guidance

**Patterns**: guidelines, guidance, best_practices, manual, handbook
**Content**: "best practices", "recommended approach", "practical guidance"
**Priority**: 70/100

### 7. **Report**
Research reports, monitoring reports, assessments, studies

**Patterns**: report, assessment, analysis, study, research, survey, monitoring
**Content**: "this report", "research findings", "methodology"
**Priority**: 50/100

### 8. **Observations**
Concluding observations from treaty monitoring bodies

**Patterns**: concluding_observations, observations
**Content**: "concluding observations", "the committee notes"
**Priority**: 85/100

### 9. **Recommendations**
Specific recommendations from committees or commissions

**Patterns**: recommendations, recommends
**Content**: "recommends that", "following recommendations"
**Priority**: 80/100

### 10. **Constitution**
National constitutions and amendments

**Patterns**: constitution, constitutional
**Content**: "constitutional court", "fundamental rights"
**Priority**: 100/100

## Classification Strategy

The classifier uses a three-stage approach with weighted scoring:

### Stage 1: Source-Based Classification (Weight: 1.0)
Direct mapping from source metadata (highest priority)

```python
source_mapping = {
    "upr": "UPR",
    "ohchr": "TreatyBodyReport",
    "acerwc": "TreatyBodyReport",
    "achpr": "TreatyBodyReport",
    "au_policy": "Policy",
    "unicef": "Report"
}
```

### Stage 2: Filename Pattern Matching (Weight: 0.8)
Regex pattern matching on normalized filename

- Filename normalization: Replace underscores and hyphens with spaces
- Case-insensitive matching
- Word boundary patterns (e.g., `\bact\b`)
- Multiple pattern matches increase score

### Stage 3: Content Keyword Matching (Weight: 0.6)
Keyword search in first 2000 characters of text

- Case-insensitive matching
- Multiple keyword matches increase score
- Weighted by document type priority

## Usage

### Basic Classification

```python
from processors.doc_classifier import DocumentClassifier

classifier = DocumentClassifier()

# Classify with source metadata (highest confidence)
doc_type, confidence, scores = classifier.classify(
    doc_id="Kenya_UPR_2020.pdf",
    source="upr"
)
# Returns: ("UPR", 1.0, {"UPR": 1.0})

# Classify by filename patterns
doc_type, confidence, scores = classifier.classify(
    doc_id="Kenya_Cyber_Security_Act_2018.pdf"
)
# Returns: ("Law", 0.72, {"Law": 0.72})

# Classify with content analysis
text = "This Act shall be known as the Data Protection Act, 2019..."
doc_type, confidence, scores = classifier.classify(
    doc_id="Data_Protection_Act.pdf",
    text_content=text
)
# Returns: ("Law", 0.85, {"Law": 0.85, "Policy": 0.21})
```

### Batch Classification

```python
documents = [
    {"doc_id": "Kenya_UPR_2020.pdf", "source": "upr"},
    {"doc_id": "Digital_Policy_2024.pdf", "source": "au_policy"},
    {"doc_id": "Cyber_Act_2018.pdf", "text_content": "..."}
]

results = classifier.classify_batch(documents)
for doc, (doc_type, confidence, scores) in zip(documents, results):
    print(f"{doc['doc_id']}: {doc_type} ({confidence:.2f})")
```

### Convenience Functions

```python
from processors.doc_classifier import classify_document, get_supported_doc_types

# Quick classification
doc_type, confidence = classify_document(
    doc_id="Kenya_Policy_2024.pdf",
    source="au_policy"
)

# Get all supported types
doc_types = get_supported_doc_types()
# Returns: ["Law", "Treaty", "TreatyBodyReport", ...]
```

## Configuration

Classification rules are defined in `configs/doc_type_rules.json`:

```json
{
  "document_types": {
    "Law": {
      "description": "Legislation, acts, statutes, regulations",
      "filename_patterns": ["\\bact\\b", "\\blaw\\b", "\\blegislation\\b"],
      "content_keywords": ["enacted by parliament", "legislative act"],
      "priority": 90
    }
  },
  "source_mapping": {
    "mapping": {
      "upr": "UPR",
      "ohchr": "TreatyBodyReport"
    }
  }
}
```

### Adding New Document Types

1. Add type definition to `configs/doc_type_rules.json`
2. Define filename patterns (regex)
3. Define content keywords
4. Set priority (0-100, higher wins conflicts)
5. Add tests to `tests/test_doc_classifier.py`
6. Run tests: `pytest tests/test_doc_classifier.py -v`

## Scoring System

Each document type has a priority (0-100). Higher priorities win in case of ties.

**Score Calculation:**
- Base score = (pattern matches / total patterns) * (priority / 100)
- Final score = (filename_score × 0.8) + (content_score × 0.6)
- Normalized to 0.0-1.0 range

**Priority Guidelines:**
- 100: Unique, high-confidence types (UPR, TreatyBodyReport, Constitution)
- 90-95: High-confidence types (Law, Treaty)
- 70-85: Medium-confidence types (Guidelines, Observations, Recommendations)
- 50-60: Lower-priority types (Report, Policy)

## Integration with Pipeline

The classifier can be integrated into the pipeline to automatically classify documents during processing:

```python
from processors.doc_classifier import classify_document

# In pipeline_runner.py or metadata management
doc_type, confidence = classify_document(
    doc_id=filename,
    source=source,
    text_content=text[:2000]  # First 2000 chars
)

# Update metadata
metadata["doc_type"] = doc_type
metadata["doc_type_confidence"] = confidence
```

## Testing

Run classifier tests:

```bash
# Run classifier tests only
pytest tests/test_doc_classifier.py -v

# Run with coverage
pytest tests/test_doc_classifier.py --cov=processors.doc_classifier --cov-report=term-missing
```

Test coverage:
- 31 tests covering all classification stages
- Source-based classification (6 tests)
- Filename pattern matching (5 tests)
- Content keyword matching (4 tests)
- Edge cases and error handling (6 tests)
- Real-world examples (4 tests)
- Batch processing (1 test)

## Performance

- **Speed**: ~0.02ms per document (filename only)
- **Speed**: ~0.5ms per document (with 2000 chars of text)
- **Batch processing**: Suitable for thousands of documents
- **Memory**: Minimal (~10KB for rules config)

## Validation Results

Tested on 78 documents from metadata:
- 77 correctly classified as "Policy" (from au_policy source)
- 1 test document (intentionally unclassified)
- **Accuracy**: 100% for source-based classification

## Limitations

1. **English-only**: Patterns and keywords are English-only
2. **First 2000 chars**: Content analysis limited to beginning of document
3. **No ML**: Rule-based approach, no machine learning (yet)
4. **Pattern dependencies**: Requires good filename/content patterns

## Future Enhancements

1. **Machine Learning**: Train ML classifier on labeled documents
2. **Multi-language**: Support for French, Spanish, Arabic patterns
3. **Deep content analysis**: Analyze full document text (with caching)
4. **Confidence calibration**: Adjust thresholds based on validation
5. **Active learning**: Learn from manual corrections
6. **Hybrid approach**: Combine rules + ML for best results

## References

- **Module**: `processors/doc_classifier.py`
- **Config**: `configs/doc_type_rules.json`
- **Tests**: `tests/test_doc_classifier.py`
- **Standards**: `docs/standards/DOC_TYPE_STANDARDS.md`
