from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.pdf_generator.serializers import PDFTemplateConfigurationSerializer, FormFieldOptionsSerializer, \
    FieldValueSerializer
from reflow_server.pdf_generator.models import PDFTemplateConfiguration
from reflow_server.pdf_generator.services import PDFGeneratorService


@method_decorator(csrf_exempt, name='dispatch')
class PDFTemplateConfigurationView(APIView):
    """
    This view is responsible for retrieving a list of PDFTemplateConfigurations for the user when he wants to edit the PDF templates
    and also accepts a POST request for CREATING a new PDF Template Configuration.

    Methods:
        GET: Returns a list of pdfs so the user can edit each of them.
        POST: Creates a single new pdf template
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form):
        instances = PDFTemplateConfiguration.pdf_generator_.pdf_template_configurations_by_user_id_company_id_and_form_name(
            request.user.id, 
            company_id, 
            form
        )
        serializer = PDFTemplateConfigurationSerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id, form):
        serializer = PDFTemplateConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user.id, company_id, form)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class PDFTemplateConfigurationEditView(APIView):
    """
    View used for updating or deleting a single pdf template configuratin id. 

    Methods:
        PUT: Updates a pdf template configuration id data.
        DELETE: Removes a pdf template configuration id data. It's important to notice that when we remove a pdf we also want
                to remove the PDF template it is bound to.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, form, pdf_template_configuration_id):
        instance = PDFTemplateConfiguration.pdf_generator_.pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(
            request.user.id, company_id, form, pdf_template_configuration_id
        )
        serializer = PDFTemplateConfigurationSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save(request.user.id, company_id, form)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, form, pdf_template_configuration_id):
        pdf_generator_service = PDFGeneratorService(request.user.id, company_id, form)
        pdf_generator_service.remove_pdf_template(pdf_template_configuration_id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


class PDFTemplatesFieldOptionsView(APIView):
    """
    View responsible for retrieving all of the field options the user can select as variables in the template.
    It's important to notice we get the fields from related formularies also. We just get the field of related formularies
    ONE level deep. So if i'm in `Pipeline Comercial` and this formulary is conected to `Cliente` we get the fields from `Cliente`.
    If `Cliente` is connected with another formulary we will not get the fields.

    Method:
        GET: Returns a list of formularies to the user and on each formulary a list of fields.
    """
    def get(self, request, company_id, form):
        pdf_generator_service = PDFGeneratorService(request.user.id, company_id, form)
        instances = pdf_generator_service.form_options_to_use_on_template
        serializer = FormFieldOptionsSerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    
class PDFTemplatesValuesOptionsView(APIView):
    def get(self, request, company_id, form, pdf_template_configuration_id, dynamic_form_id):
        pdf_generator_service = PDFGeneratorService(request.user.id, company_id, form)
        instances = pdf_generator_service.field_values_to_use_on_template(pdf_template_configuration_id, dynamic_form_id)
        serializer = FieldValueSerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)