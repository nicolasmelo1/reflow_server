from django.conf import settings

from reflow_server.core import externals


class ExtractDataWorkerExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def build_extraction_data(self):
        pass