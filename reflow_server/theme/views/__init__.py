from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.events import Event
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.pagination import Pagination
from reflow_server.theme.services import ThemeService
from reflow_server.theme.models import Theme, ThemeForm
from reflow_server.theme.serializers import ThemeSerializer, ThemeFormularySerializer
from reflow_server.formulary.models import Form


@method_decorator(csrf_exempt, name='dispatch')
class ThemeView(APIView):
    """
    This does two things, we get the theme data of a single theme
    and the other stuff is when the user selects a theme.

    Methods:
        GET: Gets a theme data based on a theme_id
        POST: Selects a theme based on a theme_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, selected_theme_id):
        instance = Theme.theme_.theme_by_theme_id(selected_theme_id)
        serializer = ThemeSerializer(instance=instance)
        Event.register_event('theme_eyeballing', {
            'user_id': request.user.id if request.user.is_authenticated else None,
            'theme_id': selected_theme_id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class SelectThemeView(APIView):
    """
    This view is responsible for selecting a theme. It automatically passes the data
    from the theme to the default user models.

    Methods:
        POST: Selects a theme based on a theme_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, selected_theme_id):
        theme = Theme.theme_.theme_by_theme_id(selected_theme_id)
        if theme:
            ThemeService.select_theme(selected_theme_id, company_id, request.user.id)
            form_name = Form.theme_.main_form_name_by_company_id_last_created(company_id)
            return Response({
                'status': 'ok',
                'data': {
                    'last_form_name': form_name
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'reason': 'theme_does_not_exist'
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ThemeFormularyView(APIView):
    """
    Retrieves the formulary from it's theme_form_id and the theme_id. 
    This data is used to preview the formulary to the user.

    Methods:
        GET: Retrives the theme form data with it's sections and fields
    """
    def get(self, request, company_id, selected_theme_id, theme_form_id):
        instance = ThemeForm.theme_.theme_form_by_theme_id_and_theme_form_id(selected_theme_id, theme_form_id)
        serializer = ThemeFormularySerializer(instance=instance, is_loading_formulary=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ThemeThemeTypeView(APIView):
    """
    Retrieves the themes by its types, types can be 'design', 'sales', 'hr', 'development' and so on
    filtered by groups of themes it can be 'reflow', 'company' or 'community'

    'reflow' - Are themes created by reflow@reflow.com.br user.
    'company' - Are themes created for and by the company, usually they are the ones that are private for the company
    'community' - Are themes created by the reflow community (all users of reflow) for the community (so public)

    Args:
        GET: Retrieves the themes of it's types (you can check `theme_type` table for reference) 
                  by each group. Since we need to know what group you are filtering `filter` query 
                  parameter is obligatory.
    """
    def get(self, request, company_id, theme_type):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1))
        )
        filter_by = request.query_params.get('filter', 'reflow')
        filter_by = filter_by if filter_by in ['reflow', 'company', 'community'] else 'reflow'
        themes = Theme.theme_.themes_by_theme_type_name(theme_type)
        if filter_by == 'reflow':
            themes = themes.filter(user_id=1, is_public=True)
        elif filter_by == 'company':
            themes = themes.filter(user__company_id=company_id, is_public=False)
        elif filter_by == 'community':
            themes = themes.filter(is_public=True).exclude(Q(user__company_id=company_id) | Q(user=1))
        __, instances = pagination.paginate_queryset(themes)
        serializer = ThemeSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
