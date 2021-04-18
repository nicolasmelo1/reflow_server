from django.conf import settings
from django.core.management.base import BaseCommand
from django.apps import apps

import os
import subprocess
import re


class Command(BaseCommand):
    help = "This command dumps all of the model `types` to fixtures/required_data.json"

    def handle(self, *args, **options):
        # get project name where all of our applications live in 
        settings_root = re.sub(r'urls$','', settings.ROOT_URLCONF)
        app_names = [app.replace(settings_root, '') for app in settings.INSTALLED_APPS if settings_root in app] 
        app_models = ['{}.{}'.format(app_label, model._meta.object_name) for app_label in app_names for model in apps.get_app_config(app_label).get_models() if re.search(r'Type$', model._meta.object_name)]
        command = 'python manage.py dumpdata {} > fixtures/required_data.json'.format(' '.join(app_models))
        print(command)
        os.system(command)
