from django.apps import AppConfig


class FormulaConfig(AppConfig):
    name = 'reflow_server.formula'

    def ready(self):
        try:
            from reflow_server.formula.services.documentation import DocumentationService

            documentation_service = DocumentationService()
            documentation_service.update_documentation()
        except Exception as e:
            print(e)