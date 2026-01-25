"""
WSGI entry point for production deployment

Use with gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

Or with other WSGI servers.
"""

import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.app import create_app  # noqa: E402

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Create application instance
app = create_app(os.getenv("FLASK_ENV", "production"))

if __name__ == "__main__":
    # This won't be used in production, but allows testing with:
    # python wsgi.py
    app.run()
