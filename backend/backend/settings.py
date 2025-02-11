import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (if present)
load_dotenv()

# ✅ Detect environment (Render sets RENDER=True)
RENDER = os.getenv("RENDER", "False").lower() == "true"

# ✅ Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secret Key (Use a secure secret in production!)
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")

# ✅ Debug mode (Enabled locally, disabled on Render)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ✅ Allowed Hosts (Prevents unauthorized access)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ✅ CORS settings (Frontend connections)
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000"
).split(",")

# ✅ Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# ✅ Logging Database Info
print(f"🔧 Running in {'Render' if RENDER else 'Local'} Mode")
print(f"📦 Database: {DATABASE_URL}")

# ✅ Installed Django Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "tests",  # Ensure your app is named correctly
]

# ✅ Middleware Stack
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ✅ URL Configuration
ROOT_URLCONF = "backend.urls"

# ✅ Template Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ✅ WSGI Application
WSGI_APPLICATION = "backend.wsgi.application"

# ✅ Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ✅ Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files (important for Render deployment)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ✅ CORS Settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Change to True if needed

# ✅ Logging Configuration (Debugging & Production Logging)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# ✅ Default Primary Key Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
