from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
        .get() -- Gets a theme data based on a theme_id
        .post() -- Selects a theme based on a theme_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, theme_id):
        instance = Theme.objects.filter(id=theme_id).first()
        serializer = ThemeSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id, theme_id):
        theme = Theme.objects.filter(id=theme_id).first()
        ThemeService.select_theme(theme, company_id, request.user.id)
        form_name = Form.objects.filter(depends_on__isnull=True, group__company_id=company_id).order_by('-created_at').values_list('form_name', flat=True).first()
        return Response({
            'status': 'ok',
            'data': {
                'last_form_name': form_name
            }
        }, status=status.HTTP_200_OK)


class ThemeFormularyView(APIView):
    def get(self, request, company_id, theme_id, theme_form_id):
        instance = ThemeForm.objects.filter(id=theme_form_id, theme_id=theme_id).first()
        serializer = ThemeFormularySerializer(instance=instance, is_loading_formulary=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class ThemeCompanyTypeView(APIView):
    def get(self, request, company_id, company_type):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1))
        )
        filter_by = request.query_params.get('filter', 'reflow')
        filter_by = filter_by if filter_by in ['reflow', 'company', 'community'] else 'reflow'
        themes = Theme.objects.filter(company_type__name=company_type)
        if filter_by == 'reflow':
            themes = themes.filter(user_id=1, is_public=True)
        elif filter_by == 'company':
            themes = themes.filter(user__company_id=company_id, is_public=False)
        elif filter_by == 'community':
            themes = themes.filter(is_public=True).exclude(Q(user__company_id=company_id) | Q(user=1))
        serializer = ThemeSerializer(instance=themes[pagination.offset:pagination.limit], many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
