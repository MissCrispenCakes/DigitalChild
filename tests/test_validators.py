"""
Tests for processors/validators.py
"""

import json
from pathlib import Path

import pytest

from processors.validators import (
    ConfigValidationError,
    FileValidationError,
    PathValidationError,
    SchemaValidationError,
    StringValidationError,
    URLValidationError,
    ValidationError,
    is_valid_iso_code,
    validate_config_has_keys,
    validate_country_name,
    validate_document_metadata,
    validate_file,
    validate_file_extension,
    validate_file_size,
    validate_json_file,
    validate_non_empty_string,
    validate_output_path,
    validate_path,
    validate_regex_pattern,
    validate_string_length,
    validate_tags_config,
    validate_url,
    validate_url_list,
)

# ========================
# URL Validation Tests
# ========================


class TestURLValidation:
    """Tests for URL validation functions."""

    def test_validate_url_valid_https(self):
        """Test validating a valid HTTPS URL."""
        url = validate_url("https://example.com")
        assert url == "https://example.com"

    def test_validate_url_valid_http(self):
        """Test validating a valid HTTP URL."""
        url = validate_url("http://example.com", allow_http=True)
        assert url == "http://example.com"

    def test_validate_url_strips_whitespace(self):
        """Test URL validation strips whitespace."""
        url = validate_url("  https://example.com  ")
        assert url == "https://example.com"

    def test_validate_url_rejects_http_when_not_allowed(self):
        """Test HTTP rejected when allow_http=False."""
        with pytest.raises(URLValidationError, match="must start with https://"):
            validate_url("http://example.com", allow_http=False)

    def test_validate_url_rejects_non_string(self):
        """Test URL validation rejects non-strings."""
        with pytest.raises(URLValidationError, match="must be a string"):
            validate_url(12345)

    def test_validate_url_rejects_empty(self):
        """Test URL validation rejects empty strings."""
        with pytest.raises(URLValidationError, match="cannot be empty"):
            validate_url("")

    def test_validate_url_rejects_no_scheme(self):
        """Test URL validation rejects URLs without scheme."""
        with pytest.raises(URLValidationError, match="must start with"):
            validate_url("example.com")

    def test_validate_url_rejects_invalid_format(self):
        """Test URL validation rejects malformed URLs."""
        with pytest.raises(URLValidationError, match="Invalid URL format"):
            validate_url("https://")

    def test_validate_url_list_valid(self):
        """Test validating a list of valid URLs."""
        urls = validate_url_list(
            ["https://example.com", "https://test.org"], allow_http=False
        )
        assert len(urls) == 2

    def test_validate_url_list_rejects_non_list(self):
        """Test URL list validation rejects non-lists."""
        with pytest.raises(URLValidationError, match="Expected list"):
            validate_url_list("not a list")

    def test_validate_url_list_identifies_bad_url(self):
        """Test URL list validation identifies which URL is bad."""
        with pytest.raises(URLValidationError, match="index 1"):
            validate_url_list(["https://example.com", "invalid", "https://test.org"])


# ========================
# Path Validation Tests
# ========================


class TestPathValidation:
    """Tests for path validation functions."""

    def test_validate_path_valid_string(self):
        """Test validating a valid path string."""
        path = validate_path("/tmp/test.txt")
        assert path == "/tmp/test.txt"

    def test_validate_path_valid_path_object(self):
        """Test validating a Path object."""
        path = validate_path(Path("/tmp/test.txt"))
        assert path == "/tmp/test.txt"

    def test_validate_path_rejects_non_string(self):
        """Test path validation rejects non-strings/non-Paths."""
        with pytest.raises(PathValidationError, match="must be string or Path"):
            validate_path(12345)

    def test_validate_path_rejects_empty(self):
        """Test path validation rejects empty strings."""
        with pytest.raises(PathValidationError, match="cannot be empty"):
            validate_path("")

    def test_validate_path_rejects_traversal(self):
        """Test path validation rejects path traversal attempts."""
        with pytest.raises(PathValidationError, match="Path traversal detected"):
            validate_path("/tmp/../etc/passwd")

    def test_validate_path_must_exist(self, tmp_path):
        """Test path validation with must_exist=True."""
        # Create a real file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should succeed
        path = validate_path(str(test_file), must_exist=True)
        assert path == str(test_file)

        # Should fail for non-existent
        with pytest.raises(PathValidationError, match="does not exist"):
            validate_path(str(tmp_path / "nonexistent.txt"), must_exist=True)

    def test_validate_path_must_be_file(self, tmp_path):
        """Test path validation with must_be_file=True."""
        # Create a real file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should succeed
        path = validate_path(str(test_file), must_be_file=True)
        assert path == str(test_file)

        # Should fail for directory
        with pytest.raises(PathValidationError, match="must be a file"):
            validate_path(str(tmp_path), must_be_file=True)

    def test_validate_path_must_be_dir(self, tmp_path):
        """Test path validation with must_be_dir=True."""
        # Should succeed
        path = validate_path(str(tmp_path), must_be_dir=True)
        assert path == str(tmp_path)

        # Create a file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should fail for file
        with pytest.raises(PathValidationError, match="must be a directory"):
            validate_path(str(test_file), must_be_dir=True)

    def test_validate_path_rejects_relative_when_not_allowed(self):
        """Test path validation rejects relative paths when not allowed."""
        with pytest.raises(PathValidationError, match="must be absolute"):
            validate_path("relative/path.txt", allow_relative=False)

    def test_validate_path_base_dir_constraint(self, tmp_path):
        """Test path validation enforces base directory constraint."""
        # Create a file inside base dir
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        # Should succeed
        path = validate_path(str(test_file), base_dir=str(tmp_path))
        assert path == str(test_file)

        # Should fail for path outside base dir
        with pytest.raises(PathValidationError, match="outside base directory"):
            validate_path("/etc/passwd", base_dir=str(tmp_path))

    def test_validate_output_path_creates_parent(self, tmp_path):
        """Test validate_output_path creates parent directories."""
        output_path = tmp_path / "subdir" / "output.txt"
        path = validate_output_path(str(output_path))
        assert path == str(output_path)
        assert output_path.parent.exists()


# ========================
# File Validation Tests
# ========================


class TestFileValidation:
    """Tests for file validation functions."""

    def test_validate_file_extension_allowed(self):
        """Test validating allowed file extensions."""
        path = validate_file_extension("test.pdf")
        assert path == "test.pdf"

    def test_validate_file_extension_rejects_disallowed(self):
        """Test rejecting disallowed file extensions."""
        with pytest.raises(FileValidationError, match="not allowed"):
            validate_file_extension("test.exe")

    def test_validate_file_extension_custom_allowed(self):
        """Test custom allowed extensions."""
        path = validate_file_extension("test.csv", allowed_extensions={".csv", ".xlsx"})
        assert path == "test.csv"

    def test_validate_file_size_within_limit(self, tmp_path):
        """Test validating file size within limit."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        path = validate_file_size(str(test_file), max_size_bytes=1000)
        assert path == str(test_file)

    def test_validate_file_size_exceeds_limit(self, tmp_path):
        """Test rejecting file that exceeds size limit."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("x" * 1000)

        with pytest.raises(FileValidationError, match="too large"):
            validate_file_size(str(test_file), max_size_bytes=100)

    def test_validate_file_size_nonexistent(self):
        """Test file size validation with nonexistent file."""
        with pytest.raises(FileValidationError, match="does not exist"):
            validate_file_size("/nonexistent/file.txt")

    def test_validate_file_comprehensive(self, tmp_path):
        """Test comprehensive file validation."""
        test_file = tmp_path / "test.pdf"
        test_file.write_text("test content")

        path = validate_file(
            str(test_file),
            must_exist=True,
            check_size=True,
            check_extension=True,
        )
        assert path == str(test_file)

    def test_validate_file_rejects_invalid(self, tmp_path):
        """Test comprehensive file validation rejects invalid files."""
        test_file = tmp_path / "test.exe"
        test_file.write_text("test")

        with pytest.raises(FileValidationError, match="not allowed"):
            validate_file(str(test_file), must_exist=True, check_extension=True)


# ========================
# String Validation Tests
# ========================


class TestStringValidation:
    """Tests for string validation functions."""

    def test_validate_non_empty_string_valid(self):
        """Test validating non-empty string."""
        result = validate_non_empty_string("hello", "test_field")
        assert result == "hello"

    def test_validate_non_empty_string_strips(self):
        """Test non-empty string validation strips whitespace."""
        result = validate_non_empty_string("  hello  ", "test_field")
        assert result == "hello"

    def test_validate_non_empty_string_rejects_non_string(self):
        """Test rejecting non-strings."""
        with pytest.raises(StringValidationError, match="must be a string"):
            validate_non_empty_string(123, "test_field")

    def test_validate_non_empty_string_rejects_empty(self):
        """Test rejecting empty strings."""
        with pytest.raises(StringValidationError, match="cannot be empty"):
            validate_non_empty_string("", "test_field")

    def test_validate_non_empty_string_rejects_whitespace_only(self):
        """Test rejecting whitespace-only strings."""
        with pytest.raises(StringValidationError, match="cannot be empty"):
            validate_non_empty_string("   ", "test_field")

    def test_validate_string_length_within_bounds(self):
        """Test validating string length within bounds."""
        result = validate_string_length("hello", min_length=3, max_length=10)
        assert result == "hello"

    def test_validate_string_length_too_short(self):
        """Test rejecting string that's too short."""
        with pytest.raises(StringValidationError, match="at least 5 characters"):
            validate_string_length("hi", min_length=5)

    def test_validate_string_length_too_long(self):
        """Test rejecting string that's too long."""
        with pytest.raises(StringValidationError, match="at most 5 characters"):
            validate_string_length("hello world", max_length=5)

    def test_validate_regex_pattern_valid(self):
        """Test validating valid regex patterns."""
        pattern = validate_regex_pattern(r"\d+")
        assert pattern == r"\d+"

    def test_validate_regex_pattern_invalid(self):
        """Test rejecting invalid regex patterns."""
        with pytest.raises(StringValidationError, match="Invalid regex"):
            validate_regex_pattern(r"[invalid(")


# ========================
# Config Validation Tests
# ========================


class TestConfigValidation:
    """Tests for config validation functions."""

    def test_validate_json_file_valid(self, tmp_path):
        """Test validating valid JSON file."""
        config_file = tmp_path / "config.json"
        config_data = {"key": "value"}
        config_file.write_text(json.dumps(config_data))

        data = validate_json_file(str(config_file))
        assert data == config_data

    def test_validate_json_file_invalid_json(self, tmp_path):
        """Test rejecting invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json {")

        with pytest.raises(ConfigValidationError, match="Invalid JSON"):
            validate_json_file(str(config_file))

    def test_validate_json_file_nonexistent(self):
        """Test rejecting nonexistent file."""
        with pytest.raises(ConfigValidationError, match="does not exist"):
            validate_json_file("/nonexistent/config.json")

    def test_validate_config_has_keys_valid(self):
        """Test validating config has required keys."""
        config = {"key1": "value1", "key2": "value2"}
        result = validate_config_has_keys(config, ["key1", "key2"])
        assert result == config

    def test_validate_config_has_keys_missing(self):
        """Test rejecting config with missing keys."""
        config = {"key1": "value1"}
        with pytest.raises(ConfigValidationError, match="missing required keys"):
            validate_config_has_keys(config, ["key1", "key2", "key3"])

    def test_validate_config_has_keys_non_dict(self):
        """Test rejecting non-dict config."""
        with pytest.raises(ConfigValidationError, match="must be a dict"):
            validate_config_has_keys(["not", "a", "dict"], ["key1"])

    def test_validate_tags_config_valid(self):
        """Test validating valid tags config."""
        config = {
            "rules": {
                "AI": [r"artificial intelligence", r"\bAI\b"],
                "ChildRights": ["child", "children"],
            }
        }
        result = validate_tags_config(config)
        assert result == config

    def test_validate_tags_config_missing_rules(self):
        """Test rejecting tags config without 'rules' key."""
        with pytest.raises(ConfigValidationError, match="missing required keys"):
            validate_tags_config({"other_key": "value"})

    def test_validate_tags_config_invalid_rules_type(self):
        """Test rejecting tags config with non-dict rules."""
        with pytest.raises(ConfigValidationError, match="'rules' must be a dict"):
            validate_tags_config({"rules": ["not", "a", "dict"]})

    def test_validate_tags_config_invalid_patterns_type(self):
        """Test rejecting tags config with non-list patterns."""
        config = {"rules": {"AI": "not a list"}}
        with pytest.raises(ConfigValidationError, match="patterns must be a list"):
            validate_tags_config(config)

    def test_validate_tags_config_invalid_regex(self):
        """Test rejecting tags config with invalid regex."""
        config = {"rules": {"AI": [r"[invalid("]}}
        with pytest.raises(ConfigValidationError, match="Invalid regex"):
            validate_tags_config(config)


# ========================
# Metadata Validation Tests
# ========================


class TestMetadataValidation:
    """Tests for metadata validation functions."""

    def test_validate_document_metadata_valid(self):
        """Test validating valid document metadata."""
        doc = {
            "id": "test-doc-1",
            "source": "au_policy",
            "year": 2024,
            "tags_history": [],
            "recommendations_history": [],
        }
        result = validate_document_metadata(doc)
        assert result == doc

    def test_validate_document_metadata_minimal(self):
        """Test validating minimal document metadata."""
        doc = {"id": "test-doc-1", "source": "au_policy"}
        result = validate_document_metadata(doc)
        assert result == doc

    def test_validate_document_metadata_missing_id(self):
        """Test rejecting metadata without id."""
        doc = {"source": "au_policy"}
        with pytest.raises(SchemaValidationError, match="missing required keys"):
            validate_document_metadata(doc)

    def test_validate_document_metadata_missing_source(self):
        """Test rejecting metadata without source."""
        doc = {"id": "test-doc-1"}
        with pytest.raises(SchemaValidationError, match="missing required keys"):
            validate_document_metadata(doc)

    def test_validate_document_metadata_empty_id(self):
        """Test rejecting metadata with empty id."""
        doc = {"id": "", "source": "au_policy"}
        with pytest.raises(SchemaValidationError, match="cannot be empty"):
            validate_document_metadata(doc)

    def test_validate_document_metadata_invalid_year(self):
        """Test rejecting metadata with invalid year."""
        doc = {"id": "test-doc-1", "source": "au_policy", "year": "not an int"}
        with pytest.raises(SchemaValidationError, match="year must be int"):
            validate_document_metadata(doc)

    def test_validate_document_metadata_year_out_of_range(self):
        """Test rejecting metadata with year out of range."""
        doc = {"id": "test-doc-1", "source": "au_policy", "year": 1800}
        with pytest.raises(SchemaValidationError, match="out of valid range"):
            validate_document_metadata(doc)

    def test_validate_document_metadata_invalid_tags_history(self):
        """Test rejecting metadata with non-list tags_history."""
        doc = {"id": "test-doc-1", "source": "au_policy", "tags_history": "not a list"}
        with pytest.raises(SchemaValidationError, match="must be a list"):
            validate_document_metadata(doc)


# ========================
# Utility Function Tests
# ========================


class TestUtilityFunctions:
    """Tests for utility validation functions."""

    def test_validate_country_name_valid(self):
        """Test validating valid country names."""
        result = validate_country_name("Kenya")
        assert result == "Kenya"

        result = validate_country_name("South Africa")
        assert result == "South Africa"

        result = validate_country_name("Cote d'Ivoire")
        assert result == "Cote d'Ivoire"

    def test_validate_country_name_rejects_empty(self):
        """Test rejecting empty country name."""
        with pytest.raises(StringValidationError, match="cannot be empty"):
            validate_country_name("")

    def test_validate_country_name_rejects_too_short(self):
        """Test rejecting country name that's too short."""
        with pytest.raises(StringValidationError, match="at least 2 characters"):
            validate_country_name("A")

    def test_validate_country_name_rejects_invalid_characters(self):
        """Test rejecting country name with invalid characters."""
        with pytest.raises(StringValidationError, match="invalid characters"):
            validate_country_name("Kenya@123")

    def test_is_valid_iso_code_valid(self):
        """Test validating valid ISO codes."""
        assert is_valid_iso_code("KE") is True
        assert is_valid_iso_code("USA") is True
        assert is_valid_iso_code("GB") is True

    def test_is_valid_iso_code_invalid(self):
        """Test rejecting invalid ISO codes."""
        assert is_valid_iso_code("K") is False
        assert is_valid_iso_code("KEEE") is False
        assert is_valid_iso_code("ke") is False  # lowercase
        assert is_valid_iso_code("123") is False
        assert is_valid_iso_code(None) is False
        assert is_valid_iso_code(123) is False


# ========================
# Exception Hierarchy Tests
# ========================


class TestExceptionHierarchy:
    """Tests for custom exception classes."""

    def test_exception_hierarchy(self):
        """Test all custom exceptions inherit from ValidationError."""
        assert issubclass(URLValidationError, ValidationError)
        assert issubclass(PathValidationError, ValidationError)
        assert issubclass(FileValidationError, ValidationError)
        assert issubclass(ConfigValidationError, ValidationError)
        assert issubclass(SchemaValidationError, ValidationError)
        assert issubclass(StringValidationError, ValidationError)

    def test_can_catch_base_exception(self):
        """Test can catch all validation errors with base class."""
        try:
            raise URLValidationError("test error")
        except ValidationError:
            pass  # Should catch it

    def test_can_catch_specific_exception(self):
        """Test can catch specific validation errors."""
        caught = False
        try:
            raise PathValidationError("test error")
        except PathValidationError:
            caught = True

        assert caught is True
