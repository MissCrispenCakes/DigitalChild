"""
Error handlers for API exceptions

Registers Flask error handlers for common exceptions and provides
custom exception classes for API errors.
"""

from flask import current_app
from werkzeug.exceptions import HTTPException

from api.utils.response import error_response
from api.utils.validators import ValidationError


class APIError(Exception):
    """Base class for API errors"""

    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "An internal error occurred"

    def __init__(self, message=None, details=None):
        # Don't pass kwargs to super() to comply with B042
        super().__init__()
        if message:
            self.message = message
        self.details = details or {}


class NotFoundError(APIError):
    """Raised when a resource is not found"""

    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class AuthenticationError(APIError):
    """Raised when authentication fails"""

    status_code = 401
    error_code = "AUTHENTICATION_FAILED"
    message = "Authentication required"


class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""

    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "Rate limit exceeded"


def register_error_handlers(app):
    """Register error handlers with Flask app"""

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle custom API errors"""
        current_app.logger.error(f"API Error: {error.message}")
        return error_response(
            message=error.message,
            code=error.error_code,
            status_code=error.status_code,
            details=error.details,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle validation errors"""
        details = {}
        if error.field:
            details["field"] = error.field

        return error_response(
            message=error.message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle Werkzeug HTTP exceptions"""
        return error_response(
            message=error.description,
            code=f"HTTP_{error.code}",
            status_code=error.code,
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors"""
        return error_response(
            message="The requested resource was not found",
            code="NOT_FOUND",
            status_code=404,
        )

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors"""
        current_app.logger.error(f"Internal error: {str(error)}")
        return error_response(
            message="An internal server error occurred",
            code="INTERNAL_ERROR",
            status_code=500,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors"""
        current_app.logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return error_response(
            message="An unexpected error occurred",
            code="INTERNAL_ERROR",
            status_code=500,
        )
