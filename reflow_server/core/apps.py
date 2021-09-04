from django.apps import AppConfig
from django.utils.autoreload import autoreload_started
from django.conf import settings

# based on this https://stackoverflow.com/a/43593959/13158385, this is some undocumented django apis.
# we need this to force the reload of the app with autoreload when non related default django files change.
def watchdog(sender, **kwargs):
    sender.watch_dir('reflow_server', '**/*.py')

class CoreConfig(AppConfig):
    name = 'reflow_server.core'

    def ready(self):
        autoreload_started.connect(watchdog)

