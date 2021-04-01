from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.authentication.models import UserExtended
from reflow_server.core.utils.pagination import Pagination
from reflow_server.formulary.services.default_attachment import DefaultAttachmentService
from reflow_server.formulary.serializers import GetFormSerializer, GetGroupSerializer, FormFieldTypeOptionsSerializer, \
    UserFieldTypeOptionsSerializer, PublicAccessFormSerializer
from reflow_server.formulary.models import Form, FormAccessedBy, Group, Field, PublicAccessForm
from reflow_server.data.models import FormValue


class GetGroupsView(APIView):
    """
    Gets the groups data, so it returns a list of groups with all of its formularies.

    Methods:
        GET: return a list of groups with all of its formularies.
    """
    def get(self, request, company_id):
        group_ids_accessed_by_user = FormAccessedBy.objects.filter(user_id=request.user.id).values_list('form__group_id', flat=True).distinct()
        instances = Group.objects.filter(id__in=group_ids_accessed_by_user, company_id=company_id, enabled=True)
        serializer = GetGroupSerializer(instance=instances, many=True, context={'user_id': request.user.id})
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class GetFormularyView(APIView):
    """
    Get the data needed to build the formulary, so this retrieves a single form, with all of it's sections and
    fields.

    Methods:
        GET: Retrieves the formulary data needed to build the formulary.
    """
    def get(self, request, company_id, form):
        instance = Form.objects.filter(form_name=form, company_id=company_id, depends_on__isnull=True).first()
        serializer = GetFormSerializer(instance=instance, context={
            'company_id': company_id,
            'public_access_key': request.query_params.get('public_key', None),
            'user_id': request.user.id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FormFieldTypeOptionsView(APIView):
    """
    View used for retrieving formulary options on `form` field_types. This retrieves all possible options, but 
    we need to optmize it with paginated options.

    Methods:
        GET: Retrieves all of the formulary options for a single field.
    """
    def get(self, request, company_id, form, field_id):
        search = request.query_params.get('search', None)
        section_id = request.query_params.get('value_id', None)
        
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )        
        form_field = Field.objects.filter(id=field_id).first()
        instances = FormValue.formulary_.form_values_by_company_id_field_id_search_value_and_form_id(
            company_id=company_id, 
            field_id=form_field.form_field_as_option, 
            search=search, 
            section_id=section_id
        )
        total_number_of_pages, instances = pagination.paginate_queryset(instances)
        serializer = FormFieldTypeOptionsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': total_number_of_pages
            },
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserFieldTypeOptionsView(APIView):
    """
    View used for retrieving all of the users of a single field. 
    If you have multiple `user` field_types you need to call it multiple times.

    Methods:
        GET: retrieves all of the users you can select for this field. 
                  right now, all of the users of a current company
    """
    def get(self, request, company_id, form, field_id):
        instances = UserExtended.formulary_.users_active_by_company_id(company_id)
        serializer = UserFieldTypeOptionsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PublicFormularyDataView(APIView):
    """
    This is a public view, this means it does not require any authentication.

    The request MUST BE public (this means it requires a public_key query param in the url)
    in order to retrieve any data.
    """
    def get(self, request, company_id, form):
        if request.is_public:
            instance = PublicAccessForm.formulary_.public_access_form_by_public_access_key_company_id_and_main_form_name(
                request.query_params.get('public_key', None),
                company_id,
                form
            )
            if instance:
                serializer = PublicAccessFormSerializer(instance=instance)
                return Response({
                    'status': 'ok',
                    'data': serializer.data
                }, status=status.HTTP_200_OK) 
            else:
                return Response({
                    'status': 'error',
                    'reason': 'does_not_exist'
                }, status=status.HTTP_400_BAD_REQUEST) 
        else: 
            return Response({
                'status': 'error'
            }, status=status.HTTP_403_FORBIDDEN)


class DefaultAttachmentToDraftView(APIView):
    def get(self, request, company_id, form, field_id, file_name):
        default_attachment_service = DefaultAttachmentService(company_id=company_id, user_id=request.user.id, field_id=field_id)
        draft_string_id = default_attachment_service.get_draft_string_id_from_default_attachment(file_name, request.is_public)
        if draft_string_id:
            return Response({
                'status': 'ok',
                'data': {
                    'draft_string_id': draft_string_id
                }
            }, status=status.HTTP_200_OK) 
        else:
            return Response({
                'status': 'error',
                'reason': 'does_not_exist'
            }, status=status.HTTP_400_BAD_REQUEST) 