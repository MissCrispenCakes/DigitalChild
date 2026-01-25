# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Flask extensions initialization

Extensions are initialized here and then imported by the app factory.
This pattern allows extensions to be configured before the app is created.
"""

from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize extensions (will be configured by app factory)
cache = Cache()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)


def init_extensions(app):
    """Initialize Flask extensions with app instance"""
    cache.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    limiter.init_app(app)
