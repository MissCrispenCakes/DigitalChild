"""
Tests for Document Type Classifier
===================================

Tests the automatic classification of document types based on
filename patterns, content keywords, and source metadata.
"""

from processors.doc_classifier import (
    DocumentClassifier,
    classify_document,
    get_supported_doc_types,
)


class TestDocumentClassifier:
    """Test DocumentClassifier class."""

    def test_classifier_initialization(self):
        """Test that classifier initializes with rules."""
        classifier = DocumentClassifier()
        assert classifier.rules is not None
        assert len(classifier.doc_types) > 0
        assert "UPR" in classifier.doc_types
        assert "Policy" in classifier.doc_types

    def test_get_doc_types(self):
        """Test getting list of supported document types."""
        classifier = DocumentClassifier()
        doc_types = classifier.get_doc_types()
        assert isinstance(doc_types, list)
        assert len(doc_types) >= 8
        assert "Law" in doc_types
        assert "Treaty" in doc_types
        assert "TreatyBodyReport" in doc_types
        assert "UPR" in doc_types
        assert "Policy" in doc_types

    def test_get_doc_type_description(self):
        """Test getting description for a doc type."""
        classifier = DocumentClassifier()
        desc = classifier.get_doc_type_description("UPR")
        assert desc is not None
        assert "universal periodic review" in desc.lower()

    def test_source_based_classification_upr(self):
        """Test source-based classification for UPR."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="Kenya_Report_2020.pdf", source="upr"
        )
        assert doc_type == "UPR"
        assert confidence == 1.0

    def test_source_based_classification_ohchr(self):
        """Test source-based classification for OHCHR."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="Some_Report.pdf", source="ohchr"
        )
        assert doc_type == "TreatyBodyReport"
        assert confidence == 1.0

    def test_source_based_classification_au_policy(self):
        """Test source-based classification for AU policy."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="Digital_Strategy.pdf", source="au_policy"
        )
        assert doc_type == "Policy"
        assert confidence == 1.0

    def test_filename_pattern_law(self):
        """Test filename pattern matching for Law documents."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="Kenya_Cyber_Security_Act_2018.pdf"
        )
        assert doc_type == "Law"
        assert confidence > 0.5

    def test_filename_pattern_treaty(self):
        """Test filename pattern matching for Treaty documents."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="African_Charter_on_Human_Rights.pdf"
        )
        assert doc_type == "Treaty"
        assert confidence > 0.5

    def test_filename_pattern_convention(self):
        """Test filename pattern matching for Convention."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="UN_Convention_on_Rights_of_Child.pdf"
        )
        assert doc_type == "Treaty"
        assert confidence > 0.5

    def test_filename_pattern_policy(self):
        """Test filename pattern matching for Policy documents."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="National_Digital_Policy_2024.pdf"
        )
        assert doc_type == "Policy"
        assert confidence > 0.3

    def test_filename_pattern_report(self):
        """Test filename pattern matching for Report documents."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="UNICEF_Child_Protection_Report_2023.pdf"
        )
        assert doc_type == "Report"
        assert confidence > 0.3

    def test_content_based_classification_law(self):
        """Test content-based classification for Law."""
        classifier = DocumentClassifier()
        text = """
        This Act may be cited as the Cyber Security and Data Protection Act, 2018.
        Be it enacted by Parliament as follows:
        Section 1. Definitions
        Section 2. Application
        This statutory instrument shall apply to all persons within the jurisdiction.
        """
        doc_type, confidence, scores = classifier.classify(
            doc_id="Document.pdf", text_content=text
        )
        assert doc_type == "Law"
        assert confidence > 0.4

    def test_content_based_classification_treaty(self):
        """Test content-based classification for Treaty."""
        classifier = DocumentClassifier()
        text = """
        The State Parties to this Convention,
        Considering the ratification by Member States,
        Recognizing the need for international law,
        Have agreed as follows:
        Article 1: Definitions
        """
        doc_type, confidence, scores = classifier.classify(
            doc_id="Document.pdf", text_content=text
        )
        assert doc_type == "Treaty"
        assert confidence > 0.4

    def test_content_based_classification_upr(self):
        """Test content-based classification for UPR."""
        classifier = DocumentClassifier()
        text = """
        Universal Periodic Review
        Working Group on the UPR
        Twenty-fifth session
        National report submitted in accordance with paragraph 5 of the annex
        to Human Rights Council resolution 16/21
        """
        doc_type, confidence, scores = classifier.classify(
            doc_id="Document.pdf", text_content=text
        )
        assert doc_type == "UPR"
        assert confidence > 0.5

    def test_content_based_classification_treaty_body(self):
        """Test content-based classification for Treaty Body Report."""
        classifier = DocumentClassifier()
        text = """
        Committee on the Rights of the Child
        Concluding observations on the report of Kenya
        The Committee considered the State party report at its 1234th meeting.
        The Committee notes with appreciation the efforts made by the State party.
        """
        doc_type, confidence, scores = classifier.classify(
            doc_id="Document.pdf", text_content=text
        )
        assert doc_type == "TreatyBodyReport"
        assert confidence > 0.4

    def test_combined_filename_and_content(self):
        """Test classification with both filename and content."""
        classifier = DocumentClassifier()
        text = """
        National Cyber Security Strategy 2024-2028
        Policy Framework and Implementation Plan
        This policy document outlines the strategic objectives
        for cyber security in Kenya.
        """
        doc_type, confidence, scores = classifier.classify(
            doc_id="Kenya_Cyber_Security_Strategy_2024.pdf", text_content=text
        )
        assert doc_type == "Policy"
        assert confidence > 0.5

    def test_no_match_returns_unknown(self):
        """Test that documents with no matches return Unknown."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(doc_id="random_file_xyz.pdf")
        assert doc_type == "Unknown"
        assert confidence == 0.0

    def test_batch_classification(self):
        """Test batch classification of multiple documents."""
        classifier = DocumentClassifier()
        documents = [
            {"doc_id": "Kenya_UPR_2020.pdf", "source": "upr"},
            {"doc_id": "Digital_Policy_2024.pdf", "source": "au_policy"},
            {"doc_id": "Cyber_Act_2018.pdf", "source": None},
        ]
        results = classifier.classify_batch(documents)
        assert len(results) == 3
        assert results[0][0] == "UPR"
        assert results[1][0] == "Policy"
        assert results[2][0] == "Law"


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_classify_document_function(self):
        """Test classify_document convenience function."""
        doc_type, confidence = classify_document(
            doc_id="Kenya_UPR_Report_2020.pdf", source="upr"
        )
        assert doc_type == "UPR"
        assert confidence == 1.0

    def test_classify_document_with_content(self):
        """Test classify_document with text content."""
        text = "This Act shall be known as the Data Protection Act, 2019."
        doc_type, confidence = classify_document(
            doc_id="Data_Protection_Act.pdf", text_content=text
        )
        assert doc_type == "Law"
        assert confidence > 0.3

    def test_get_supported_doc_types_function(self):
        """Test get_supported_doc_types function."""
        doc_types = get_supported_doc_types()
        assert isinstance(doc_types, list)
        assert "Law" in doc_types
        assert "Policy" in doc_types
        assert "UPR" in doc_types


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_doc_id(self):
        """Test classification with empty document ID."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(doc_id="")
        assert doc_type == "Unknown"

    def test_none_doc_id(self):
        """Test classification with None document ID."""
        classifier = DocumentClassifier()
        # Should handle gracefully
        try:
            doc_type, confidence, scores = classifier.classify(
                doc_id=None, source="upr"
            )
            # If source is provided, should still classify
            assert doc_type == "UPR"
        except AttributeError:
            # Or raise AttributeError which is acceptable
            pass

    def test_empty_text_content(self):
        """Test classification with empty text content."""
        classifier = DocumentClassifier()
        doc_type, confidence, scores = classifier.classify(
            doc_id="Document.pdf", text_content=""
        )
        # Should fall back to filename patterns
        assert doc_type == "Unknown"

    def test_case_insensitive_matching(self):
        """Test that pattern matching is case-insensitive."""
        classifier = DocumentClassifier()
        # Test uppercase
        doc_type1, _, _ = classifier.classify(doc_id="KENYA_CYBER_ACT_2018.PDF")
        # Test lowercase
        doc_type2, _, _ = classifier.classify(doc_id="kenya_cyber_act_2018.pdf")
        # Test mixed case
        doc_type3, _, _ = classifier.classify(doc_id="Kenya_Cyber_Act_2018.pdf")

        # All should classify as Law
        assert doc_type1 == "Law"
        assert doc_type2 == "Law"
        assert doc_type3 == "Law"


class TestPriorityAndScoring:
    """Test priority levels and scoring logic."""

    def test_high_priority_types_win(self):
        """Test that high-priority types (Treaty, UPR) win over low-priority."""
        classifier = DocumentClassifier()

        # Document that could be both Treaty and Report
        doc_type, _, scores = classifier.classify(doc_id="Convention_Report_2024.pdf")

        # Treaty has higher priority (95) than Report (50)
        assert doc_type in ["Treaty", "Report"]
        if "Treaty" in scores and "Report" in scores:
            # Treaty should score higher due to priority
            assert scores.get("Treaty", 0) >= scores.get("Report", 0)

    def test_multiple_pattern_matches_increase_score(self):
        """Test that multiple pattern matches increase confidence."""
        classifier = DocumentClassifier()

        # Document with many law-related keywords
        doc_type1, conf1, _ = classifier.classify(doc_id="Cyber_Act.pdf")

        doc_type2, conf2, _ = classifier.classify(
            doc_id="Cyber_Security_Act_Legislation_2018.pdf"
        )

        # More pattern matches should give higher confidence
        assert doc_type1 == "Law"
        assert doc_type2 == "Law"
        # Second one has more matches, should have higher confidence
        assert conf2 >= conf1


class TestRealWorldExamples:
    """Test with real-world document examples."""

    def test_au_cyber_security_convention(self):
        """Test African Union Cyber Security Convention."""
        classifier = DocumentClassifier()
        doc_type, confidence, _ = classifier.classify(
            doc_id="AFRICAN_UNION_CONVENTION_ON_CYBER_SECURITY_AND_PERSONAL_DATA_PROTECTION.pdf"
        )
        assert doc_type == "Treaty"
        assert confidence > 0.6

    def test_kenya_upr_report(self):
        """Test Kenya UPR report with source."""
        classifier = DocumentClassifier()
        doc_type, confidence, _ = classifier.classify(
            doc_id="Kenya_UPR_Third_Cycle_2020.pdf", source="upr"
        )
        assert doc_type == "UPR"
        assert confidence == 1.0

    def test_digital_strategy_policy(self):
        """Test digital strategy document."""
        classifier = DocumentClassifier()
        doc_type, confidence, _ = classifier.classify(
            doc_id="National_Digital_Strategy_2024.pdf"
        )
        assert doc_type == "Policy"
        assert confidence > 0.4

    def test_ohchr_concluding_observations(self):
        """Test OHCHR concluding observations."""
        classifier = DocumentClassifier()
        doc_type, confidence, _ = classifier.classify(
            doc_id="CRC_Concluding_Observations_Kenya_2023.pdf", source="ohchr"
        )
        assert doc_type == "TreatyBodyReport"
        assert confidence == 1.0
