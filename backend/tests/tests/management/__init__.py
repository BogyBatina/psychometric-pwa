import os
import logging

if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

try:
    import django
    django.setup()
except Exception as e:
    print(f"⚠️ Django setup failed: {e}")

logger = logging.getLogger(__name__)

if os.getenv("DEBUG", "True").lower() in ["true", "1"]:
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("🚀 Backend initialized in DEBUG mode.")
else:
    logging.basicConfig(level=logging.INFO)
    logger.info("🔒 Backend running in PRODUCTION mode.")

def initialize_backend():
    """Initialize backend-specific components if needed."""
    logger.info("🔧 Running backend initialization...")

if not hasattr(os.environ, "INITIALIZED"):
    os.environ["INITIALIZED"] = "1"
    initialize_backend()
