from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.events import Event
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.pagination import Pagination
from reflow_server.formulary.models import Form
from reflow_server.pdf_generator.serializers import PDFTemplateConfigurationSerializer, FormFieldOptionsSerializer, \
    FieldValueSerializer, PDFTemplateAllowedTextBlockSerializer, PDFTemplateConfigurationManySerializer
from reflow_server.pdf_generator.models import PDFTemplateConfiguration, PDFGenerated, PDFTemplateAllowedTextBlock
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
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )    
        instances = PDFTemplateConfiguration.pdf_generator_.pdf_template_configurations_by_user_id_company_id_and_form_name_ordered_by_id(
            request.user.id, 
            company_id, 
            form
        )
        total_number_of_pages, instances = pagination.paginate_queryset(instances)
        serializer = PDFTemplateConfigurationManySerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': total_number_of_pages
            },
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id, form):
        serializer = PDFTemplateConfigurationSerializer(data=request.data)
        if serializer.is_valid(request.user.id, company_id, form):
            serializer.save()
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
        GET: Get a single PDF template data so the user can edit it
        PUT: Updates a pdf template configuration id data.
        DELETE: Removes a pdf template configuration id data. It's important to notice that when we remove a pdf we also want
                to remove the PDF template it is bound to.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form, pdf_template_configuration_id):
        instance = PDFTemplateConfiguration.pdf_generator_.pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(
            request.user.id, company_id, form, pdf_template_configuration_id
        )
        serializer = PDFTemplateConfigurationSerializer(instance=instance)
        return Response({
                'status': 'ok',
                'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, company_id, form, pdf_template_configuration_id):
        instance = PDFTemplateConfiguration.pdf_generator_.pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(
            request.user.id, company_id, form, pdf_template_configuration_id
        )
        serializer = PDFTemplateConfigurationSerializer(data=request.data, instance=instance)
        if serializer.is_valid(request.user.id, company_id, form):
            serializer.save()
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
        instances, form_from_connected_field_helper = pdf_generator_service.form_options_to_use_on_template
        serializer = FormFieldOptionsSerializer(instances, many=True, context={'form_from_connected_field_helper': form_from_connected_field_helper})
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    
class PDFTemplatesValuesOptionsView(APIView):
    """
    Responsible for retrieving the data of a formulary by it's dynamic_form_id and the pdf_template_configuration_id.
    What we do is first get the variables of the template, with this we can save some resources when retriving
    the data.
    Then what this does is get the variables data of a template. (variables data is the actual data of the fields
    selected as variables from the dynamic_form_id) 

    Methods:
        GET: Returns an array of objects, each object is a FormValue instance that holds the value for each field_id
        that is used as variable.
    """
    def get(self, request, company_id, form, pdf_template_configuration_id, dynamic_form_id):
        pdf_generator_service = PDFGeneratorService(request.user.id, company_id, form)
        instances, form_value_from_connected_field_helper = pdf_generator_service.field_values_to_use_on_template(pdf_template_configuration_id, dynamic_form_id)
        serializer = FieldValueSerializer(instances, many=True, context={'form_value_from_connected_field_helper': form_value_from_connected_field_helper})
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PDFTemplatesForReaderView(APIView):
    """
    Responsible for retrieving a list of templates from the formulary. It's important to understand
    that the templates retrieved are from the company. And not from the user. All of the templates, are
    for the hole company, they are never private.

    Methods:
        GET: Returns a list of templates bounded to a form and from a single company_id
    """
    def get(self, request, company_id, form):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )
        instances = PDFTemplateConfiguration.pdf_generator_.pdf_template_configurations_by_company_id_and_form_name_ordered_by_id(
            company_id, 
            form
        )
        total_number_of_pages, instances = pagination.paginate_queryset(instances)
        serializer = PDFTemplateConfigurationManySerializer(instances, many=True)
        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': total_number_of_pages
            },
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PDFTemplateGetDataForReaderView(APIView):
    """
    Responsible for retrieving the rich text data alongside with everything needed to render the PDF Template, so we can mount it on the page and the user can 
    download it.

    Methods:
        GET: Retrieves a single PDFTemplate so we get the rich text data. Improving the performance of the list.
    """
    def get(self, request, company_id, form, pdf_template_configuration_id):
        instance = PDFTemplateConfiguration.pdf_generator_.pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(
            request.user.id, company_id, form, pdf_template_configuration_id
        )
        serializer = PDFTemplateConfigurationSerializer(instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class PDFGenerateView(APIView):
    """
    This view is only for billing, we check if the user can download pdf template before downloading.

    Methods:
        GET: Checks if the user can download or not the PDF template. This View is reponsible just for saving
        what template_id was used for downloading the pdf, on what company and what user made the download. This way
        we can control and analyse the downloads.
    """
    def get(self, request, company_id, form, pdf_template_configuration_id):
        form = Form.pdf_generator_.formulary_by_company_id_and_form_name(company_id, form)
        PDFGenerated.pdf_generator_.create(
            company_id,
            request.user.id,
            pdf_template_configuration_id
        )
        Event.register_event('pdf_template_downloaded', {
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form.id if form else None,
            'pdf_template_id': pdf_template_configuration_id
        })
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


class PDFTemplateAllowedTextBlockView(APIView):
    """
    View responsible for retrieving the allowed blocks that the PDF template can handle. Other block types
    will not be supported. So when trying to save a PDFTemplate with an unsuported block type it will fail.

    Methods:
        GET: The allowed Text blocks that the PDF Template can handle, other block types will not be supported
        so it will fail when saving the data.
    """
    def get(self, request):
        instance = PDFTemplateAllowedTextBlock.pdf_generator_.all_pdf_template_allowed_text_blocks()
        serializer = PDFTemplateAllowedTextBlockSerializer(instance=instance, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
