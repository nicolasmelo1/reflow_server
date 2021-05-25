from django.core.management.base import BaseCommand

import subprocess


class Command(BaseCommand):
    help = "Since we use git trees, i thought it would be easier to create a single command for pushing code"

    def handle(self, *args, **options):
        # get project name where all of our applications live in 
        subprocess.run(['git', 'push']) 
        subprocess.run(['git', 'subtree', 'push', '--prefix', 'extensions/reflow_formula_field', 'reflow_formula_field', 'main'])
