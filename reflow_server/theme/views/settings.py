from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.pagination import Pagination
from reflow_server.theme.serializers.settings import ThemeSettingsSerializer
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
        themes = Theme.theme_.themes_by_user_and_company(company_id, request.user.id)
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
        serializer = ThemeSettingsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)


class ThemeSettingsDependentFormulariesView(APIView):
    def get(self, request, company_id):
        dependent_form_ids = ThemeService.get_dependent_formularies(company_id)
        return Response({
            'status': 'ok',
            'data': dependent_form_ids
        }, status=status.HTTP_200_OK)