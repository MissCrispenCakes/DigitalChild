"""
Configuration management for DigitalChild API

Loads settings from environment variables with sensible defaults
for development, production, and testing environments.
"""

import os
from pathlib import Path


class Config:
    """Base configuration with common settings"""

    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # API settings
    API_KEYS = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []
    API_VERSION = "v1"

    # CORS settings
    CORS_ORIGINS = (
        os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if os.getenv("CORS_ORIGINS")
        else ["http://localhost:3000"]
    )
    CORS_SUPPORTS_CREDENTIALS = True

    # Caching settings
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))

    # Rate limiting settings
    RATELIMIT_STORAGE_URL = os.getenv("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "100 per hour")
    RATELIMIT_AUTHENTICATED = os.getenv("RATELIMIT_AUTHENTICATED", "1000 per hour")

    # Data file paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    METADATA_FILE = os.getenv(
        "METADATA_FILE", str(DATA_DIR / "metadata" / "metadata.json")
    )
    SCORECARD_FILE = os.getenv(
        "SCORECARD_FILE", str(DATA_DIR / "scorecard" / "scorecard_main.xlsx")
    )
    TAGS_CONFIG_DIR = os.getenv("TAGS_CONFIG_DIR", str(PROJECT_ROOT / "configs"))
    EXPORTS_DIR = os.getenv("EXPORTS_DIR", str(DATA_DIR / "exports"))

    # Pagination defaults
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    TESTING = False

    # More verbose logging
    LOG_LEVEL = "DEBUG"

    # Shorter cache timeouts for development
    CACHE_DEFAULT_TIMEOUT = 60


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False

    # Override with environment variables (required in production)
    SECRET_KEY = os.getenv("SECRET_KEY")
    API_KEYS = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []

    # Use Redis for caching in production
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")

    # Use Redis for rate limiting in production
    RATELIMIT_STORAGE_URL = os.getenv(
        "RATELIMIT_STORAGE_URL", "redis://localhost:6379/1"
    )

    @staticmethod
    def validate():
        """Validate production configuration"""
        if not os.getenv("SECRET_KEY"):
            raise ValueError("SECRET_KEY must be set in production")
        if not os.getenv("API_KEYS"):
            raise ValueError("API_KEYS must be set in production")


class TestingConfig(Config):
    """Testing environment configuration"""

    DEBUG = True
    TESTING = True

    # Use simple cache for tests
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 1

    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False

    # Use test data files
    METADATA_FILE = str(Config.PROJECT_ROOT / "tests" / "fixtures" / "metadata.json")
    SCORECARD_FILE = str(
        Config.PROJECT_ROOT / "tests" / "fixtures" / "scorecard_test.xlsx"
    )


# Config selector
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env_name=None):
    """Get configuration based on environment name"""
    if env_name is None:
        env_name = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env_name, DevelopmentConfig)
