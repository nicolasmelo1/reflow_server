from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.pagination import Pagination
from reflow_server.formulary.models import Form
from reflow_server.theme.serializers.settings import ThemeSettingsSerializer, FormularyOptionSerializer
from reflow_server.theme.services import ThemeService
from reflow_server.theme.models import Theme


@method_decorator(csrf_exempt, name='dispatch')
class ThemeSettingsView(APIView):
    """
    Responsible for retrieving the theme data and for saving new themes.

    Methods:
        GET: Retrieve the theme data so the user can edit. It has pagination, it is only 15 items per page. Use `page`
        query parameter to change the page.
        POST: Creates a new template based on the formularies the user has selected.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )
        themes = Theme.theme_.themes_by_user_and_company_ordered_by_id(company_id, request.user.id)
        total_number_of_pages, instances = pagination.paginate_queryset(themes)
        serializer = ThemeSettingsSerializer(instance=instances, many=True)

        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': total_number_of_pages
            },
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = ThemeSettingsSerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id
        })

        if serializer.is_valid():
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
class ThemeSettingsEditView(APIView):
    """
    Used for editing or deleting a template data. It's important to understand the user CANNOT
    edit the formularies directly, he needs to add all of the formularies again if he wants to edit, add
    or remove a formulary from a template.

    Methods:
        PUT: Changes a template based on the theme_id recieved. The user CANNOT edit the formularies of the template
        directly, for editing, adding or removing formularies of a template the user needs to select the formularies
        again.
        DELETE: Deletes a template based on its id, nothing fancy
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, theme_id):
        instance = Theme.theme_.theme_by_theme_id(theme_id)
        serializer = ThemeSettingsSerializer(data=request.data, instance=instance, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, theme_id):
        instance = Theme.theme_.theme_by_theme_id(theme_id)
        instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


class ThemeFormulariesOptionsView(APIView):
    """
    Responsible for getting the formulary data the user can select inside of a template.
    He only can select those formularies he has access to, and also if a formulary he has access
    depends on a formulary he DOES NOT have access he can't select this formulary.

    Methods:
        GET: Gets a list of formularies the user can select for his templates.
    """
    def get(self, request, company_id):
        form_ids_options_for_user = ThemeService.get_forms_the_user_can_select(company_id, request.user.id)
        instances = Form.theme_.main_forms_by_company_id_and_form_ids(company_id, form_ids_options_for_user)
        serializer = FormularyOptionSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ThemeSettingsDependentFormulariesView(APIView):
    """
    Gets the formularies ids that depends on others. Returns a dict with each key being a dependent formulary
    and the values is a list of formulary ids it depends on.

    This might be confused with depends_on on Form. But it's not this. This dependent formularies are main forms
    that have `form` field types. These field types are usually connected to another formulary. We use this because
    when creating themes, if we select a formulary that depends on other, we actually need to select it's dependencies.

    Methods:
        GET: Gets the dependent formulary ids. Those that are dependent are the keys, and the values of the key is a list of the
        formularies ids it depends on
    """
    def get(self, request, company_id):
        dependent_form_ids = ThemeService.get_dependent_formularies(company_id)
        return Response({
            'status': 'ok',
            'data': dependent_form_ids
        }, status=status.HTTP_200_OK)