from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.serializers import GetFormSerializer, GetGroupSerializer, FormFieldTypeOptionsSerializer, \
    UserFieldTypeOptionsSerializer
from reflow_server.formulary.models import Form, FormAccessedBy, Group, Field
from reflow_server.data.models import FormValue


class GetGroupsView(APIView):
    """
    Gets the groups data, so it returns a list of groups with all of its formularies.

    Methods:
        .get() -- return a list of groups with all of its formularies.
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
        .get() -- Retrieves the formulary data needed to build the formulary.
    """
    def get(self, request, company_id, form):
        instance = Form.objects.filter(form_name=form, company_id=company_id, depends_on__isnull=True).first()
        serializer = GetFormSerializer(user_id=request.user.id, instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class FormFieldTypeOptionsView(APIView):
    """
    View used for retrieving formulary options on `form` field_types. This retrieves all possible options, but 
    we need to optmize it with paginated options.

    Methods:
        .get() -- Retrieves all of the formulary options for a single field.
    """
    def get(self, request, company_id, form, field_id):
        form_field = Field.objects.filter(id=field_id).first()
        instances = FormValue.objects.filter(company_id=company_id, field_id=form_field.form_field_as_option)
        serializer = FormFieldTypeOptionsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserFieldTypeOptionsView(APIView):
    """
    View used for retrieving all of the users of a single field. 
    If you have multiple `user` field_types you need to call it multiple times.

    Methods:
        .get() -- retrieves all of the users you can select for this field. 
                  right now, all of the users of a current company
    """
    def get(self, request, company_id, form, field_id):
        instances = UserExtended.objects.filter(company_id=company_id, is_active=True)
        serializer = UserFieldTypeOptionsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)