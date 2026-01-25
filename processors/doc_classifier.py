"""
Document Type Classifier
========================

Automatic classification of document types based on filename patterns,
content keywords, and source metadata.

Supported document types:
- Law: Legislation, acts, statutes, regulations
- Treaty: International treaties, conventions, charters
- TreatyBodyReport: UN treaty body reports (OHCHR, CRC, etc.)
- UPR: Universal Periodic Review documents
- Policy: Government policies, strategies, frameworks
- Guidelines: Best practices, recommendations
- Report: Research reports, assessments, studies
- Observations: Concluding observations from treaty bodies
- Recommendations: Specific recommendations
- Constitution: National constitutions

Classification Strategy:
1. Source-based: Direct mapping from source metadata (highest priority)
2. Filename patterns: Regex matching on document ID/filename
3. Content keywords: Keyword search in document text (first 2000 chars)

Returns confidence score and classified type.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple

from processors.logger import get_logger

logger = get_logger(__name__)

# Default rules file location
DEFAULT_RULES_FILE = "configs/doc_type_rules.json"


class DocumentClassifier:
    """
    Classifies documents into types based on rules-based approach.
    """

    def __init__(self, rules_file: str = DEFAULT_RULES_FILE):
        """
        Initialize classifier with rules from JSON config.

        Args:
            rules_file: Path to doc_type_rules.json
        """
        self.rules_file = rules_file
        self.rules = self._load_rules()
        self.doc_types = self.rules.get("document_types", {})
        self.source_mapping = self.rules.get("source_mapping", {}).get("mapping", {})
        self.default_type = (
            self.rules.get("classification_strategy", {}).get(
                "default_type", "Unknown"
            )
        )
        logger.info(f"Initialized classifier with {len(self.doc_types)} document types")

    def _load_rules(self) -> Dict:
        """Load classification rules from JSON file."""
        if not os.path.exists(self.rules_file):
            logger.error(f"Rules file not found: {self.rules_file}")
            return {}

        with open(self.rules_file, "r", encoding="utf-8") as f:
            rules = json.load(f)
            logger.debug(f"Loaded rules version {rules.get('version', 'unknown')}")
            return rules

    def classify(
        self,
        doc_id: str,
        source: Optional[str] = None,
        text_content: Optional[str] = None,
    ) -> Tuple[str, float, Dict[str, float]]:
        """
        Classify a document based on available information.

        Args:
            doc_id: Document filename/ID
            source: Source of the document (e.g., 'upr', 'au_policy')
            text_content: First few thousand characters of document text

        Returns:
            Tuple of (doc_type, confidence, scores_by_type)
            - doc_type: Best matching document type
            - confidence: Confidence score (0.0 to 1.0)
            - scores_by_type: Dict of all types with their scores

        Examples:
            >>> classifier = DocumentClassifier()
            >>> doc_type, conf, _ = classifier.classify(
            ...     doc_id="Kenya_UPR_2020.pdf",
            ...     source="upr"
            ... )
            >>> assert doc_type == "UPR"
            >>> assert conf == 1.0
        """
        scores = {}

        # Stage 1: Source-based classification (highest priority)
        if source and source in self.source_mapping:
            doc_type = self.source_mapping[source]
            logger.debug(f"Source-based classification: {source} → {doc_type}")
            return doc_type, 1.0, {doc_type: 1.0}

        # Stage 2: Filename pattern matching
        filename_scores = self._classify_by_filename(doc_id)
        for dt, score in filename_scores.items():
            scores[dt] = scores.get(dt, 0.0) + score * 0.8

        # Stage 3: Content keyword matching
        if text_content:
            content_scores = self._classify_by_content(text_content)
            for dt, score in content_scores.items():
                scores[dt] = scores.get(dt, 0.0) + score * 0.6

        # Normalize scores
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                scores = {dt: s / max_score for dt, s in scores.items()}

        # Get best match
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type]
            logger.debug(
                f"Classified '{doc_id}' as {best_type} (confidence: {confidence:.2f})"
            )
            return best_type, confidence, scores
        else:
            logger.debug(f"No classification match for '{doc_id}', using default")
            return self.default_type, 0.0, {}

    def _classify_by_filename(self, filename: str) -> Dict[str, float]:
        """
        Score document types based on filename patterns.

        Args:
            filename: Document filename or ID

        Returns:
            Dict mapping doc_type to score (0.0 to 1.0)
        """
        scores = {}
        # Normalize filename: lowercase and replace underscores/hyphens with spaces
        # This allows word boundary patterns to work correctly
        filename_normalized = filename.lower().replace("_", " ").replace("-", " ")

        for doc_type, config in self.doc_types.items():
            patterns = config.get("filename_patterns", [])
            matches = 0

            for pattern in patterns:
                if re.search(pattern, filename_normalized, re.IGNORECASE):
                    matches += 1

            if matches > 0:
                # Score based on number of pattern matches and priority
                priority = config.get("priority", 50) / 100.0
                base_score = min(matches / len(patterns), 1.0) if patterns else 0.0
                scores[doc_type] = base_score * priority

        return scores

    def _classify_by_content(self, text: str, max_chars: int = 2000) -> Dict[str, float]:
        """
        Score document types based on content keywords.

        Args:
            text: Document text content
            max_chars: Maximum characters to analyze (default: 2000)

        Returns:
            Dict mapping doc_type to score (0.0 to 1.0)
        """
        scores = {}
        # Only analyze first N characters for performance
        text_sample = text[:max_chars].lower()

        for doc_type, config in self.doc_types.items():
            keywords = config.get("content_keywords", [])
            matches = 0

            for keyword in keywords:
                if keyword.lower() in text_sample:
                    matches += 1

            if matches > 0:
                # Score based on keyword match ratio and priority
                priority = config.get("priority", 50) / 100.0
                base_score = min(matches / len(keywords), 1.0) if keywords else 0.0
                scores[doc_type] = base_score * priority

        return scores

    def classify_batch(
        self, documents: List[Dict]
    ) -> List[Tuple[str, float, Dict[str, float]]]:
        """
        Classify multiple documents at once.

        Args:
            documents: List of dicts with keys: doc_id, source, text_content

        Returns:
            List of (doc_type, confidence, scores) tuples
        """
        results = []
        for doc in documents:
            result = self.classify(
                doc_id=doc.get("doc_id", ""),
                source=doc.get("source"),
                text_content=doc.get("text_content"),
            )
            results.append(result)
        return results

    def get_doc_types(self) -> List[str]:
        """Return list of all supported document types."""
        return list(self.doc_types.keys())

    def get_doc_type_description(self, doc_type: str) -> Optional[str]:
        """Get description for a specific document type."""
        return self.doc_types.get(doc_type, {}).get("description")


# Convenience functions for pipeline integration


def classify_document(
    doc_id: str,
    source: Optional[str] = None,
    text_content: Optional[str] = None,
    rules_file: str = DEFAULT_RULES_FILE,
) -> Tuple[str, float]:
    """
    Classify a single document (convenience function).

    Args:
        doc_id: Document filename/ID
        source: Source of the document
        text_content: Document text content
        rules_file: Path to rules config

    Returns:
        Tuple of (doc_type, confidence)
    """
    classifier = DocumentClassifier(rules_file=rules_file)
    doc_type, confidence, _ = classifier.classify(doc_id, source, text_content)
    return doc_type, confidence


def get_supported_doc_types(rules_file: str = DEFAULT_RULES_FILE) -> List[str]:
    """
    Get list of all supported document types.

    Args:
        rules_file: Path to rules config

    Returns:
        List of document type names
    """
    classifier = DocumentClassifier(rules_file=rules_file)
    return classifier.get_doc_types()
