import os
import logging

# ✅ Setup Django settings module
if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# ✅ Import Django after setting environment variables
try:
    import django
    from django.conf import settings
    django.setup()  # Ensures Django is initialized properly
except Exception as e:
    print(f"⚠️ Django setup failed: {e}")

# ✅ Configure logging for debugging
logger = logging.getLogger(__name__)

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("🚀 Backend initialized in DEBUG mode.")
else:
    logging.basicConfig(level=logging.INFO)
    logger.info("🔒 Backend running in PRODUCTION mode.")

# ✅ Custom initialization logic (if needed)
def initialize_backend():
    """Initialize backend-specific components if needed."""
    logger.info("🔧 Running backend initialization...")

# ✅ Run initialization (only if not already running)
if not hasattr(settings, "INITIALIZED"):
    settings.INITIALIZED = True
    initialize_backend()
