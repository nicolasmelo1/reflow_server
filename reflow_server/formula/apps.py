from django.apps import AppConfig


class FormulaConfig(AppConfig):
    name = 'reflow_server.formula'

    def ready(self):
        from reflow_server.formula.services.documentation import DocumentationService

        documentation_service = DocumentationService()
        documentation_service.update_documentation()