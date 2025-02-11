import os
import sys

# Set the correct settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
