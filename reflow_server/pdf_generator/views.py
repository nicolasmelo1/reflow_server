from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.pdf_generator.serializers import PDFTemplateConfigurationSerializer, FieldOptionsSerializer
from reflow_server.pdf_generator.models import PDFTemplateConfiguration
from reflow_server.pdf_generator.services import PDFGeneratorService


class PDFTemplateConfigurationView(APIView):
    def get(self, request, company_id, form):
        instances = PDFTemplateConfiguration.pdf_generator_.pdf_template_configuration_by_user_id_company_id_and_form_name(
            request.user.id, 
            company_id, 
            form
        )
        serializer = PDFTemplateConfigurationSerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PDFTemplatesFieldOptionsView(APIView):
    def get(self, request, company_id, form):
        pdf_generator_service = PDFGeneratorService(request.user.id, company_id, form)
        instances = pdf_generator_service.field_options_to_use_on_template
        serializer = FieldOptionsSerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)