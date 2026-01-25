# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Request parameter validators

Provides validation functions for API request parameters.
"""

from typing import Any, List, Optional


class ValidationError(Exception):
    """Raised when request validation fails"""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message, field)
        self.message = message
        self.field = field


def validate_page(value: Any, default: int = 1) -> int:
    """
    Validate page number parameter

    Args:
        value: Page number from request
        default: Default value if not provided

    Returns:
        Validated page number (>= 1)

    Raises:
        ValidationError: If page is invalid
    """
    if value is None:
        return default

    try:
        page = int(value)
        if page < 1:
            raise ValidationError("Page must be >= 1", field="page")
        return page
    except ValueError:
        raise ValidationError("Page must be an integer", field="page")


def validate_per_page(value: Any, default: int = 20, max_value: int = 100) -> int:
    """
    Validate per_page parameter

    Args:
        value: Items per page from request
        default: Default value if not provided
        max_value: Maximum allowed value

    Returns:
        Validated per_page number

    Raises:
        ValidationError: If per_page is invalid
    """
    if value is None:
        return default

    try:
        per_page = int(value)
        if per_page < 1:
            raise ValidationError("per_page must be >= 1", field="per_page")
        if per_page > max_value:
            raise ValidationError(f"per_page must be <= {max_value}", field="per_page")
        return per_page
    except ValueError:
        raise ValidationError("per_page must be an integer", field="per_page")


def validate_integer(
    value: Any,
    field_name: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> Optional[int]:
    """
    Validate integer parameter

    Args:
        value: Integer value from request
        field_name: Name of field for error messages
        min_value: Minimum allowed value (optional)
        max_value: Maximum allowed value (optional)

    Returns:
        Validated integer or None if not provided

    Raises:
        ValidationError: If integer is invalid
    """
    if value is None:
        return None

    try:
        int_value = int(value)
        if min_value is not None and int_value < min_value:
            raise ValidationError(
                f"{field_name} must be >= {min_value}", field=field_name
            )
        if max_value is not None and int_value > max_value:
            raise ValidationError(
                f"{field_name} must be <= {max_value}", field=field_name
            )
        return int_value
    except ValueError:
        raise ValidationError(f"{field_name} must be an integer", field=field_name)


def validate_year(value: Any) -> Optional[int]:
    """
    Validate year parameter

    Args:
        value: Year from request

    Returns:
        Validated year or None if not provided

    Raises:
        ValidationError: If year is invalid
    """
    if value is None:
        return None

    try:
        year = int(value)
        if year < 1900 or year > 2100:
            raise ValidationError("Year must be between 1900 and 2100", field="year")
        return year
    except ValueError:
        raise ValidationError("Year must be an integer", field="year")


def validate_enum(
    value: Any, allowed_values: List[str], field_name: str
) -> Optional[str]:
    """
    Validate enum parameter against allowed values

    Args:
        value: Value from request
        allowed_values: List of allowed values
        field_name: Name of field for error messages

    Returns:
        Validated value or None if not provided

    Raises:
        ValidationError: If value not in allowed_values
    """
    if value is None:
        return None

    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of: {', '.join(allowed_values)}",
            field=field_name,
        )

    return value


def validate_string(
    value: Any, field_name: str, max_length: int = 200
) -> Optional[str]:
    """
    Validate string parameter

    Args:
        value: String value from request
        field_name: Name of field for error messages
        max_length: Maximum allowed length

    Returns:
        Validated string or None if not provided

    Raises:
        ValidationError: If string is invalid
    """
    if value is None:
        return None

    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string", field=field_name)

    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} must be <= {max_length} characters", field=field_name
        )

    return value.strip()
