# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Flask application factory

Creates and configures the Flask app with all extensions,
blueprints, and error handlers.
"""

import logging

from flask import Flask

from api.config import get_config
from api.extensions import init_extensions
from api.middleware.error_handlers import register_error_handlers


def create_app(config_name=None):
    """
    Application factory for creating Flask app instances

    Args:
        config_name: Configuration name ("development", "production", "testing")

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Validate production configuration
    if hasattr(config_class, "validate"):
        config_class.validate()

    # Configure logging
    setup_logging(app)

    # Initialize extensions
    init_extensions(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    register_blueprints(app)

    # Log startup info
    app.logger.info(f"Starting DigitalChild API v{app.config['API_VERSION']}")
    app.logger.info(f"Environment: {app.config['FLASK_ENV']}")
    app.logger.info(f"Debug mode: {app.debug}")

    return app


def register_blueprints(app):
    """Register Flask blueprints (route modules)"""
    from api.routes.documents import documents_bp
    from api.routes.export import export_bp
    from api.routes.health import health_bp
    from api.routes.scorecard import scorecard_bp
    from api.routes.tags import tags_bp
    from api.routes.timeline import timeline_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(scorecard_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(timeline_bp)
    app.register_blueprint(export_bp)

    app.logger.info(f"Registered {len(app.blueprints)} blueprints")


def setup_logging(app):
    """Configure application logging"""
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"))

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=app.config.get("LOG_FORMAT"),
    )

    # Set Flask app logger level
    app.logger.setLevel(log_level)

    # Silence noisy third-party loggers
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
