# Validators Module Usage Guide

The `processors/validators.py` module provides centralized validation functions for URLs, paths, files, configs, and data throughout the DigitalChild project.

## Benefits

- **Centralized**: All validation logic in one place
- **Consistent**: Same validation rules across the codebase
- **Secure**: Prevents path traversal, validates input types, checks bounds
- **Clear Errors**: Custom exception classes with descriptive messages
- **Well-Tested**: 68 comprehensive tests ensuring reliability

## Exception Hierarchy

```python
ValidationError  # Base exception
├── URLValidationError
├── PathValidationError
├── FileValidationError
├── ConfigValidationError
├── SchemaValidationError
└── StringValidationError
```

All validators raise specific exceptions that inherit from `ValidationError`, allowing you to catch all validation errors or specific types.

## Quick Examples

### URL Validation

```python
from processors.validators import validate_url, URLValidationError

try:
    # Validate and normalize URL
    url = validate_url("https://example.com")

    # Allow HTTP URLs
    url = validate_url("http://example.com", allow_http=True)

    # Validate list of URLs
    urls = validate_url_list([
        "https://example.com",
        "https://test.org"
    ])

except URLValidationError as e:
    logger.error(f"Invalid URL: {e}")
```

### Path Validation

```python
from processors.validators import validate_path, validate_output_path, PathValidationError

try:
    # Basic path validation
    path = validate_path("/tmp/file.txt")

    # Require path to exist
    path = validate_path("/tmp/file.txt", must_exist=True)

    # Require path to be a file
    path = validate_path("/tmp/file.txt", must_be_file=True)

    # Prevent path traversal and require within base directory
    path = validate_path(
        user_input_path,
        base_dir="/safe/directory",
        allow_relative=False
    )

    # Validate output path (creates parent directories if needed)
    output_path = validate_output_path("data/exports/report.csv")

except PathValidationError as e:
    logger.error(f"Invalid path: {e}")
```

### File Validation

```python
from processors.validators import validate_file, validate_file_extension, FileValidationError

try:
    # Comprehensive file validation
    filepath = validate_file(
        "document.pdf",
        must_exist=True,
        check_size=True,
        check_extension=True
    )

    # Check extension only
    validate_file_extension("document.pdf")

    # Custom allowed extensions
    validate_file_extension(
        "data.csv",
        allowed_extensions={".csv", ".xlsx"}
    )

    # Check file size (default 100MB limit)
    validate_file_size("large_file.pdf", max_size_bytes=50*1024*1024)

except FileValidationError as e:
    logger.error(f"Invalid file: {e}")
```

### String Validation

```python
from processors.validators import (
    validate_non_empty_string,
    validate_string_length,
    validate_regex_pattern,
    StringValidationError
)

try:
    # Non-empty string (strips whitespace)
    value = validate_non_empty_string(user_input, "username")

    # Length constraints
    password = validate_string_length(
        user_input,
        min_length=8,
        max_length=128,
        field_name="password"
    )

    # Validate regex pattern
    pattern = validate_regex_pattern(r"\d{4}", "year pattern")

except StringValidationError as e:
    logger.error(f"Invalid string: {e}")
```

### Config Validation

```python
from processors.validators import (
    validate_json_file,
    validate_config_has_keys,
    validate_tags_config,
    ConfigValidationError
)

try:
    # Load and validate JSON file
    config = validate_json_file("configs/settings.json")

    # Check required keys
    validate_config_has_keys(
        config,
        required_keys=["version", "rules"],
        config_name="settings"
    )

    # Validate tags configuration structure
    tags_config = validate_json_file("configs/tags_v3.json")
    validate_tags_config(tags_config)

except ConfigValidationError as e:
    logger.error(f"Invalid config: {e}")
```

### Metadata Schema Validation

```python
from processors.validators import validate_document_metadata, SchemaValidationError

try:
    doc = {
        "id": "doc-123",
        "source": "au_policy",
        "year": 2024,
        "tags_history": []
    }

    validated_doc = validate_document_metadata(doc)

except SchemaValidationError as e:
    logger.error(f"Invalid metadata: {e}")
```

### Country Name Validation

```python
from processors.validators import validate_country_name, is_valid_iso_code

try:
    # Validate country name
    country = validate_country_name("Kenya")

    # Check if valid ISO code
    if is_valid_iso_code("KE"):
        print("Valid ISO code")

except StringValidationError as e:
    logger.error(f"Invalid country: {e}")
```

## Integration Examples

### Before (Manual Validation)

```python
def process_url(url):
    if not url or not isinstance(url, str):
        return {"error": "Invalid URL"}

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return {"error": "URL must have scheme"}

    # Process URL...
```

### After (Using Validators)

```python
from processors.validators import validate_url, URLValidationError

def process_url(url):
    try:
        url = validate_url(url, allow_http=True)
    except URLValidationError as e:
        return {"error": str(e)}

    # Process URL...
```

## Security Features

### Path Traversal Prevention

```python
# ✅ Safe - rejects path traversal
try:
    validate_path("/data/../../etc/passwd")
except PathValidationError:
    # Raises: "Path traversal detected"
    pass
```

### Base Directory Constraint

```python
# ✅ Safe - ensures path is within allowed directory
try:
    validate_path(
        user_provided_path,
        base_dir="/var/app/data"
    )
except PathValidationError:
    # Raises if path is outside /var/app/data
    pass
```

### File Size Limits

```python
# ✅ Safe - prevents large file attacks
try:
    validate_file_size("upload.pdf", max_size_bytes=10*1024*1024)  # 10MB
except FileValidationError:
    # Raises if file exceeds 10MB
    pass
```

## Best Practices

1. **Always use validators for external input**

   ```python
   # User input, API responses, file uploads, etc.
   url = validate_url(user_input_url)
   ```

1. **Catch specific exceptions when possible**

   ```python
   try:
       validate_file(filepath)
   except FileValidationError as e:
       logger.error(f"File validation failed: {e}")
   except ValidationError as e:
       logger.error(f"General validation failed: {e}")
   ```

1. **Provide context in field names**

   ```python
   # Good
   validate_non_empty_string(value, "username")

   # Bad
   validate_non_empty_string(value, "value")
   ```

1. **Validate early, fail fast**

   ```python
   def process_document(filepath, output_dir):
       # Validate inputs immediately
       filepath = validate_file(filepath, must_exist=True)
       output_dir = validate_path(output_dir, must_be_dir=True)

       # Then process
       ...
   ```

1. **Use base_dir for user-controlled paths**

   ```python
   # Prevent directory traversal attacks
   safe_path = validate_path(
       user_path,
       base_dir="/safe/uploads",
       allow_relative=False
   )
   ```

## Testing

Run validator tests:

```bash
pytest tests/test_validators.py -v
```

All 68 tests cover:

- URL validation (11 tests)
- Path validation (11 tests)
- File validation (8 tests)
- String validation (10 tests)
- Config validation (9 tests)
- Metadata validation (9 tests)
- Utility functions (7 tests)
- Exception hierarchy (3 tests)

## API Reference

See `processors/validators.py` for complete API documentation with docstrings for all functions.

### Core Functions

- `validate_url()` - URL validation
- `validate_path()` - Path validation with security checks
- `validate_file()` - Comprehensive file validation
- `validate_non_empty_string()` - String presence validation
- `validate_string_length()` - String length bounds
- `validate_regex_pattern()` - Regex syntax validation
- `validate_json_file()` - JSON file loading and validation
- `validate_config_has_keys()` - Config structure validation
- `validate_tags_config()` - Tags config validation
- `validate_document_metadata()` - Metadata schema validation

### Utility Functions

- `is_valid_iso_code()` - Check ISO country code format
- `validate_country_name()` - Country name validation

## Migration Guide

When adding validation to existing code:

1. Import the validators
1. Replace manual validation with validator calls
1. Update exception handling to use specific exception types
1. Add tests for the validated code paths

See `processors/scorecard_validator.py` and `processors/tagger.py` for real examples of migration.
