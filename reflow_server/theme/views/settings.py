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
    View responsible for retrieving the theme data and for saving new themes.
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
    def get(self, request, company_id):
        form_ids_options_for_user = ThemeService.get_forms_the_user_can_select(company_id, request.user.id)
        instances = Form.theme_.main_forms_by_company_id_and_form_ids(company_id, form_ids_options_for_user)
        serializer = FormularyOptionSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ThemeSettingsDependentFormulariesView(APIView):
    def get(self, request, company_id):
        dependent_form_ids = ThemeService.get_dependent_formularies(company_id)
        return Response({
            'status': 'ok',
            'data': dependent_form_ids
        }, status=status.HTTP_200_OK)