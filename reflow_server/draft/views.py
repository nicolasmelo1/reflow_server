from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.parsers import FormParser, MultiPartParser
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.draft.services import DraftService
from reflow_server.draft.serializer import DraftValueSerializer


@method_decorator(csrf_exempt, name='dispatch')
class DraftSaveFileView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, company_id):
        files = [request.data.getlist(key) for key in request.data.keys()]
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        draft_id = draft_service.save_new_draft(draft_file=files[0][0] if len(files) > 0 else None)
        return Response({
            'status': 'ok',
            'data': {
                'draft_id': draft_id
            }
        })
        

@method_decorator(csrf_exempt, name='dispatch')
class DraftEditFileView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, company_id, draft_string_id):
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        url = draft_service.draft_file_url_by_draft_string_id(draft_string_id)
        return redirect(url)


@method_decorator(csrf_exempt, name='dispatch')
class DraftSaveValueView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        serializer = DraftValueSerializer(data=request.data)
        draft_id = serializer.save(company_id=company_id, user_id=request.user.id)
        return Response({
            'status': 'ok',
            'data': {
                'draft_id': draft_id
            }
        })



