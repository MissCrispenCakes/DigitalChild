# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Centralized Validation Module
------------------------------
Provides validation functions for URLs, paths, configs, and data.
Includes custom exception classes for clear error handling.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

# Maximum file size: 100MB
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024

# Allowed file extensions for document processing
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".html", ".htm", ".txt", ".json"}


# ========================
# Custom Exception Classes
# ========================


class ValidationError(Exception):
    """Base exception for all validation errors."""

    pass


class URLValidationError(ValidationError):
    """Raised when URL validation fails."""

    pass


class PathValidationError(ValidationError):
    """Raised when path validation fails."""

    pass


class FileValidationError(ValidationError):
    """Raised when file validation fails."""

    pass


class ConfigValidationError(ValidationError):
    """Raised when config validation fails."""

    pass


class SchemaValidationError(ValidationError):
    """Raised when schema validation fails."""

    pass


class StringValidationError(ValidationError):
    """Raised when string validation fails."""

    pass


# ========================
# URL Validation
# ========================


def validate_url(url: Any, allow_http: bool = True, require_scheme: bool = True) -> str:
    """
    Validate and normalize a URL.

    Args:
        url: URL to validate (must be string)
        allow_http: Allow http:// in addition to https://
        require_scheme: Require URL to have http:// or https:// scheme

    Returns:
        Normalized URL string (stripped of whitespace)

    Raises:
        URLValidationError: If URL is invalid
    """
    # Check type
    if not isinstance(url, str):
        raise URLValidationError(f"URL must be a string, got {type(url).__name__}")

    # Check empty
    url = url.strip()
    if not url:
        raise URLValidationError("URL cannot be empty")

    # Check scheme
    if require_scheme:
        allowed_schemes = ["https://"]
        if allow_http:
            allowed_schemes.append("http://")

        if not any(url.startswith(scheme) for scheme in allowed_schemes):
            schemes_str = " or ".join(allowed_schemes)
            raise URLValidationError(f"URL must start with {schemes_str}")

    # Parse URL to validate structure
    try:
        parsed = urlparse(url)
        if require_scheme and not parsed.netloc:
            raise URLValidationError(f"Invalid URL format: {url}")
    except Exception as e:
        raise URLValidationError(f"Failed to parse URL: {e}")

    return url


def validate_url_list(urls: List[Any], **kwargs) -> List[str]:
    """
    Validate a list of URLs.

    Args:
        urls: List of URLs to validate
        **kwargs: Additional arguments passed to validate_url()

    Returns:
        List of validated URLs

    Raises:
        URLValidationError: If any URL is invalid
    """
    if not isinstance(urls, list):
        raise URLValidationError(f"Expected list, got {type(urls).__name__}")

    validated = []
    for i, url in enumerate(urls):
        try:
            validated.append(validate_url(url, **kwargs))
        except URLValidationError as e:
            raise URLValidationError(f"URL at index {i} invalid: {e}")

    return validated


# ========================
# Path Validation
# ========================


def validate_path(
    path: Any,
    must_exist: bool = False,
    must_be_file: bool = False,
    must_be_dir: bool = False,
    allow_relative: bool = True,
    base_dir: Optional[str] = None,
) -> str:
    """
    Validate a file system path.

    Args:
        path: Path to validate
        must_exist: Path must exist on filesystem
        must_be_file: Path must be a file (implies must_exist)
        must_be_dir: Path must be a directory (implies must_exist)
        allow_relative: Allow relative paths
        base_dir: If provided, ensure path is within this base directory

    Returns:
        Validated path string

    Raises:
        PathValidationError: If path is invalid
    """
    # Check type
    if not isinstance(path, (str, Path)):
        raise PathValidationError(
            f"Path must be string or Path, got {type(path).__name__}"
        )

    path_str = str(path).strip()
    if not path_str:
        raise PathValidationError("Path cannot be empty")

    # Convert to Path object for validation
    path_obj = Path(path_str)

    # Check for path traversal attempts
    if ".." in path_obj.parts:
        raise PathValidationError(f"Path traversal detected: {path_str}")

    # Check absolute vs relative
    if not allow_relative and not path_obj.is_absolute():
        raise PathValidationError(f"Path must be absolute: {path_str}")

    # Check existence
    if must_be_file:
        must_exist = True
        if path_obj.exists() and not path_obj.is_file():
            raise PathValidationError(f"Path must be a file: {path_str}")

    if must_be_dir:
        must_exist = True
        if path_obj.exists() and not path_obj.is_dir():
            raise PathValidationError(f"Path must be a directory: {path_str}")

    if must_exist and not path_obj.exists():
        raise PathValidationError(f"Path does not exist: {path_str}")

    # Check base directory constraint
    if base_dir:
        base_path = Path(base_dir).resolve()
        try:
            resolved_path = path_obj.resolve()
            if not str(resolved_path).startswith(str(base_path)):
                raise PathValidationError(
                    f"Path {path_str} is outside base directory {base_dir}"
                )
        except (OSError, RuntimeError) as e:
            raise PathValidationError(f"Failed to resolve path {path_str}: {e}")

    return path_str


def validate_output_path(path: Any, base_dir: Optional[str] = None) -> str:
    """
    Validate a path for writing output files.

    Args:
        path: Output path to validate
        base_dir: If provided, ensure path is within this base directory

    Returns:
        Validated path string

    Raises:
        PathValidationError: If path is invalid
    """
    path_str = validate_path(
        path, must_exist=False, allow_relative=True, base_dir=base_dir
    )

    # Ensure parent directory exists or can be created
    path_obj = Path(path_str)
    parent = path_obj.parent

    if not parent.exists():
        try:
            parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PathValidationError(
                f"Cannot create parent directory for {path_str}: {e}"
            )

    return path_str


# ========================
# File Validation
# ========================


def validate_file_extension(
    filepath: str, allowed_extensions: Optional[set] = None
) -> str:
    """
    Validate file has an allowed extension.

    Args:
        filepath: Path to file
        allowed_extensions: Set of allowed extensions (e.g., {'.pdf', '.txt'})
                          If None, uses ALLOWED_EXTENSIONS

    Returns:
        Validated filepath

    Raises:
        FileValidationError: If extension is not allowed
    """
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS

    ext = Path(filepath).suffix.lower()
    if ext not in allowed_extensions:
        raise FileValidationError(
            f"File extension '{ext}' not allowed. Allowed: {sorted(allowed_extensions)}"
        )

    return filepath


def validate_file_size(filepath: str, max_size_bytes: Optional[int] = None) -> str:
    """
    Validate file size is within limits.

    Args:
        filepath: Path to file
        max_size_bytes: Maximum file size in bytes (default: MAX_FILE_SIZE_BYTES)

    Returns:
        Validated filepath

    Raises:
        FileValidationError: If file is too large
    """
    if max_size_bytes is None:
        max_size_bytes = MAX_FILE_SIZE_BYTES

    if not os.path.exists(filepath):
        raise FileValidationError(f"File does not exist: {filepath}")

    size = os.path.getsize(filepath)
    if size > max_size_bytes:
        max_mb = max_size_bytes / (1024 * 1024)
        actual_mb = size / (1024 * 1024)
        raise FileValidationError(
            f"File too large: {actual_mb:.2f}MB exceeds limit of {max_mb:.2f}MB"
        )

    return filepath


def validate_file(
    filepath: str,
    must_exist: bool = True,
    check_size: bool = True,
    check_extension: bool = True,
    allowed_extensions: Optional[set] = None,
    max_size_bytes: Optional[int] = None,
) -> str:
    """
    Comprehensive file validation.

    Args:
        filepath: Path to file
        must_exist: File must exist
        check_size: Check file size limits
        check_extension: Check file extension
        allowed_extensions: Set of allowed extensions
        max_size_bytes: Maximum file size

    Returns:
        Validated filepath

    Raises:
        FileValidationError: If file validation fails
    """
    # Validate path
    try:
        filepath = validate_path(filepath, must_exist=must_exist, must_be_file=True)
    except PathValidationError as e:
        raise FileValidationError(str(e))

    # Check extension
    if check_extension:
        validate_file_extension(filepath, allowed_extensions)

    # Check size
    if check_size and must_exist:
        validate_file_size(filepath, max_size_bytes)

    return filepath


# ========================
# String Validation
# ========================


def validate_non_empty_string(
    value: Any, field_name: str = "value", strip: bool = True
) -> str:
    """
    Validate value is a non-empty string.

    Args:
        value: Value to validate
        field_name: Name of field for error messages
        strip: Strip whitespace before checking

    Returns:
        Validated string (stripped if strip=True)

    Raises:
        StringValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise StringValidationError(
            f"{field_name} must be a string, got {type(value).__name__}"
        )

    result = value.strip() if strip else value
    if not result:
        raise StringValidationError(f"{field_name} cannot be empty")

    return result


def validate_string_length(
    value: str,
    min_length: int = 0,
    max_length: Optional[int] = None,
    field_name: str = "value",
) -> str:
    """
    Validate string length is within bounds.

    Args:
        value: String to validate
        min_length: Minimum length (inclusive)
        max_length: Maximum length (inclusive), None for no limit
        field_name: Name of field for error messages

    Returns:
        Validated string

    Raises:
        StringValidationError: If length is out of bounds
    """
    if not isinstance(value, str):
        raise StringValidationError(
            f"{field_name} must be a string, got {type(value).__name__}"
        )

    length = len(value)

    if length < min_length:
        raise StringValidationError(
            f"{field_name} must be at least {min_length} characters, got {length}"
        )

    if max_length is not None and length > max_length:
        raise StringValidationError(
            f"{field_name} must be at most {max_length} characters, got {length}"
        )

    return value


def validate_regex_pattern(pattern: str, field_name: str = "pattern") -> str:
    """
    Validate a string is a valid regex pattern.

    Args:
        pattern: Regex pattern to validate
        field_name: Name of field for error messages

    Returns:
        Validated pattern

    Raises:
        StringValidationError: If pattern is invalid
    """
    try:
        re.compile(pattern)
    except re.error as e:
        raise StringValidationError(f"Invalid regex {field_name}: {e}")

    return pattern


# ========================
# JSON/Config Validation
# ========================


def validate_json_file(filepath: str) -> Dict[str, Any]:
    """
    Validate and load a JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        ConfigValidationError: If file is invalid or cannot be parsed
    """
    # Validate path
    try:
        validate_file(filepath, must_exist=True, check_extension=False)
    except FileValidationError as e:
        raise ConfigValidationError(f"Invalid config file path: {e}")

    # Load and parse JSON
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigValidationError(f"Invalid JSON in {filepath}: {e}")
    except PermissionError:
        raise ConfigValidationError(f"Permission denied reading {filepath}")
    except Exception as e:
        raise ConfigValidationError(f"Failed to read {filepath}: {e}")

    return data


def validate_config_has_keys(
    config: Dict[str, Any], required_keys: List[str], config_name: str = "config"
) -> Dict[str, Any]:
    """
    Validate config dict has required keys.

    Args:
        config: Config dictionary to validate
        required_keys: List of required keys
        config_name: Name of config for error messages

    Returns:
        Validated config

    Raises:
        ConfigValidationError: If required keys are missing
    """
    if not isinstance(config, dict):
        raise ConfigValidationError(
            f"{config_name} must be a dict, got {type(config).__name__}"
        )

    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ConfigValidationError(
            f"{config_name} missing required keys: {missing_keys}"
        )

    return config


def validate_tags_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate tags configuration structure.

    Args:
        config: Tags config to validate

    Returns:
        Validated config

    Raises:
        ConfigValidationError: If config is invalid
    """
    # Check required top-level key
    validate_config_has_keys(config, ["rules"], "tags config")

    # Validate rules structure
    rules = config["rules"]
    if not isinstance(rules, dict):
        raise ConfigValidationError(
            f"tags config 'rules' must be a dict, got {type(rules).__name__}"
        )

    # Validate each rule
    for tag_name, patterns in rules.items():
        if not isinstance(tag_name, str):
            raise ConfigValidationError(f"Tag name must be string, got {tag_name}")

        if not isinstance(patterns, list):
            raise ConfigValidationError(
                f"Tag '{tag_name}' patterns must be a list, got {type(patterns).__name__}"
            )

        # Validate each pattern is a valid regex
        for i, pattern in enumerate(patterns):
            if not isinstance(pattern, str):
                raise ConfigValidationError(
                    f"Tag '{tag_name}' pattern {i} must be string"
                )
            try:
                validate_regex_pattern(pattern, f"tag '{tag_name}' pattern {i}")
            except StringValidationError as e:
                raise ConfigValidationError(str(e))

    return config


# ========================
# Metadata Schema Validation
# ========================


def validate_document_metadata(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate document metadata structure.

    Args:
        doc: Document metadata to validate

    Returns:
        Validated metadata

    Raises:
        SchemaValidationError: If metadata is invalid
    """
    # Check required fields
    required_fields = ["id", "source"]
    try:
        validate_config_has_keys(doc, required_fields, "document metadata")
    except ConfigValidationError as e:
        raise SchemaValidationError(str(e))

    # Validate id is non-empty string
    try:
        validate_non_empty_string(doc["id"], "document id")
    except StringValidationError as e:
        raise SchemaValidationError(str(e))

    # Validate source is non-empty string
    try:
        validate_non_empty_string(doc["source"], "document source")
    except StringValidationError as e:
        raise SchemaValidationError(str(e))

    # Validate optional fields if present
    if "year" in doc and doc["year"] is not None:
        if not isinstance(doc["year"], int):
            raise SchemaValidationError(
                f"year must be int, got {type(doc['year']).__name__}"
            )
        if doc["year"] < 1900 or doc["year"] > 2100:
            raise SchemaValidationError(f"year {doc['year']} out of valid range")

    if "tags_history" in doc:
        if not isinstance(doc["tags_history"], list):
            raise SchemaValidationError("tags_history must be a list")

    if "recommendations_history" in doc:
        if not isinstance(doc["recommendations_history"], list):
            raise SchemaValidationError("recommendations_history must be a list")

    return doc


# ========================
# Utility Functions
# ========================


def validate_country_name(country: str) -> str:
    """
    Validate country name is a reasonable string.

    Args:
        country: Country name to validate

    Returns:
        Validated country name

    Raises:
        StringValidationError: If invalid
    """
    country = validate_non_empty_string(country, "country name")
    validate_string_length(
        country, min_length=2, max_length=100, field_name="country name"
    )

    # Basic sanity check: no special characters except spaces, hyphens, apostrophes
    if not re.match(r"^[A-Za-z\s\-']+$", country):
        raise StringValidationError(
            f"Country name contains invalid characters: {country}"
        )

    return country


def is_valid_iso_code(code: str) -> bool:
    """
    Check if string looks like a valid ISO country code.

    Args:
        code: Code to check

    Returns:
        True if code matches ISO format (2 or 3 uppercase letters)
    """
    if not isinstance(code, str):
        return False

    return bool(re.match(r"^[A-Z]{2,3}$", code))
