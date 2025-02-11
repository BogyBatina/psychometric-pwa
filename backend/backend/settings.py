import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Detect environment (Render sets RENDER=True automatically)
RENDER = os.getenv("RENDER", "False").lower() == "true"

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

if RENDER:  # If running on Render, use PostgreSQL
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:  # Local development uses SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(os.path.dirname(__file__), "db.sqlite3"),
        }
    }

print(f"🔧 Running in {'Render' if RENDER else 'Local'} Mode")
print(f"📦 Database: {DATABASE_URL}")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Ignore error in production

