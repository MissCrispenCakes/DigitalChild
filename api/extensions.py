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

# Limiter initialized with default key_func, will be reconfigured in init_extensions
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")


def init_extensions(app):
    """Initialize Flask extensions with app instance"""
    from api.middleware.rate_limit import get_rate_limit_key

    cache.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Reconfigure limiter with custom key function
    limiter._key_func = get_rate_limit_key
    limiter._storage_uri = app.config.get("RATELIMIT_STORAGE_URI", "memory://")
    limiter.init_app(app)
