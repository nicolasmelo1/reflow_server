from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.draft.services import DraftService

@method_decorator(csrf_exempt, name='dispatch')
class APIDraftSaveFileExternalView(APIView):
    """
    Exactly the same as the `DraftSaveFileView` except this handles the draft for the api instead of the internal user.

    This makes it easier for us to handle the file uploads for the api and add any new logic if needed.

    Methods:
        POST: Save a new draft for the api.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, company_id):
        files = [request.data.getlist(key) for key in request.data.keys()]
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        draft_string_id = draft_service.save_new_draft(
            draft_file=files[0][0] if len(files) > 0 else None, 
            is_public_draft=False
        )
        return Response({
            'status': 'ok',
            'data': {
                'draft_string_id': draft_string_id
            }
        }, status=status.HTTP_200_OK)

class DraftRemoveDraftExternalView(APIView):
    def get(self, request):
        DraftService.remove_old_drafts()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)