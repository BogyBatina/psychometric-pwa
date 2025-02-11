import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Detect environment (Render sets RENDER=True automatically)
RENDER = os.getenv("RENDER", "False").lower() == "true"

# Database configuration
import os
import dj_database_url

DATABASE_URL = os.getenv("DATABASE_URL")  # Get from environment variables

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Use SQLite as a fallback
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Ignore error in production

