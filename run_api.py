#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 GRIMdata / LittleRainbowRights
# SPDX-License-Identifier: MIT

"""
Development server entry point

Runs the Flask development server with hot reloading.
NOT for production use - use wsgi.py with gunicorn instead.
"""

import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.app import create_app  # noqa: E402

if __name__ == "__main__":
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv not installed, skipping .env file")

    # Create app
    app = create_app("development")

    # Run development server
    host = os.getenv("DEV_HOST", "127.0.0.1")
    port = int(os.getenv("DEV_PORT", "5000"))

    print(f"\n{'='*60}")
    print("DigitalChild API - Development Server")
    print(f"{'='*60}")
    print(f"Environment: {app.config['FLASK_ENV']}")
    print(f"Debug mode: {app.debug}")
    print(f"URL: http://{host}:{port}")
    print(f"Health check: http://{host}:{port}/api/health")
    print(f"{'='*60}\n")

    app.run(host=host, port=port, debug=True)
