from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.serializers.settings import GroupSerializer
from reflow_server.formulary.models import Group


@method_decorator(csrf_exempt, name='dispatch')
class GroupSettings(APIView):
    def get(self, request, company_id):
        instances = Group.objects.filter(company=company_id)
        serializer = GroupSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        })

