from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = "List all URL patterns in the project"

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        url_patterns = resolver.url_patterns

        for pattern in url_patterns:
            self.stdout.write(str(pattern))
