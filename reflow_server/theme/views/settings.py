from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.pagination import Pagination
from reflow_server.theme.serializers.settings import ThemeSettingsSerializer
from reflow_server.theme.models import Theme


@method_decorator(csrf_exempt, name='dispatch')
class ThemeSettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )
        themes = Theme.theme_.themes_by_user_and_company(company_id, request.user.id)
        instances = pagination.paginate_queryset(themes)
        serializer = ThemeSettingsSerializer(instance=instances, many=True)

        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': pagination.get_total_number_of_pages(themes.count())
            },
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ThemeSettingsIsDependentFormView(APIView):
    def get(self, request, company_id, form_id):
        pass