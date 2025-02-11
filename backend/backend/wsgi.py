import os
from django.core.wsgi import get_wsgi_application

# ✅ Set the default settings module for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# ✅ Expose the WSGI callable as a module-level variable named "application"
application = get_wsgi_application()
