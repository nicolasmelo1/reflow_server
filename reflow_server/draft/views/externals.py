from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.draft.services import DraftService


class DraftRemoveDraftExternalView(APIView):
    def get(self, request):
        DraftService.remove_old_drafts()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)