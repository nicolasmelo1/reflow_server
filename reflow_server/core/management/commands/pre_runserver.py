from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps

from reflow_server.formula.services.documentation import DocumentationService


class Command(BaseCommand):
    help = "This command is supposed to run BEFORE the runserver command. So add this in your dockerfile and your docker-compose"
    def handle(self, *args, **options):
        # update the documentation
        documentation_service = DocumentationService()
        documentation_service.update_documentation()