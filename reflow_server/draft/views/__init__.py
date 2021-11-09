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
    """
    This view is responsible for saving a new draft file to the drafts. 
    As you might already know, drafts are always temporary, so this draft
    will be removed after some time. Be aware of this and make sure you subscribe
    to the webhook so you can know the file was deleted and want to save the file again. 

    Methods:
        POST: Recieves a formencoded data with the file. This WILL NOT recieve any data.
               everything here is considered as FILES.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, company_id):
        files = [request.data.getlist(key) for key in request.data.keys()]
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        draft_string_id = draft_service.save_new_draft(
            draft_file=files[0][0] if len(files) > 0 else None, 
            is_public_draft=request.is_public
        )
        return Response({
            'status': 'ok',
            'data': {
                'draft_string_id': draft_string_id
            }
        }, status=status.HTTP_200_OK)
        

@method_decorator(csrf_exempt, name='dispatch')
class DraftEditFileView(APIView):
    """
    View responsible for retriving a draft file temporary url. When we save a file in the draft
    it stays on our storage service temporarily, but we might need to display or even download this
    file while it is in the draft. That's exactly why we use this. We get a temporary url from the draft
    to the file.

    Methods:
        GET: redirects the user to a temporary url for the file in the storage service
             that we use
        PUT: Modifies the file in amazon s3 with a new file.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, company_id, draft_string_id):
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        url = draft_service.draft_file_url_by_draft_string_id(draft_string_id)
        if url != '': 
            return redirect(url)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, company_id, draft_string_id):
        files = [request.data.getlist(key) for key in request.data.keys()]
        draft_id = DraftService.draft_id_from_draft_string_id(draft_string_id=draft_string_id)
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        draft_string_id = draft_service.save_new_draft(
            draft_file=files[0][0] if len(files) > 0 else None, 
            draft_id=draft_id,
            is_public_draft=request.is_public
        )
        return Response({
            'status': 'ok',
            'data': {
                'draft_string_id': draft_string_id
            }
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class DraftSaveValueView(APIView):
    """
    Really similar to `DraftSaveFileView` but instead what we do here is save a value.
    This value is ALWAYS a string. Whenever you want to save a data or any other stuff temporarily
    you should consider this view. This expects a JSON with `value` as the only key.

    Methods:
        POST: Saves a string value to the draft.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        serializer = DraftValueSerializer(data=request.data)
        draft_id = serializer.save(company_id=company_id, user_id=request.user.id)
        return Response({
            'status': 'ok',
            'data': {
                'draft_string_id': draft_id
            }
        }, status=status.HTTP_200_OK)


class DraftRemoveDraftView(APIView):
    """
    View responsible for removing the draft. This is used when a component is unmounting in the client
    side. Or when we don't want to use the draft anymore, basically. When this happens we need to
    remove the draft

    Methods:
        DELETE: Deletes a draft instance by it's `draft_string_id`
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def delete(self, request, company_id, draft_string_id):
        draft_service = DraftService(company_id=company_id, user_id=request.user.id)
        draft_id = DraftService.draft_id_from_draft_string_id(draft_string_id=draft_string_id)
        draft_service.remove_draft_by_draft_id(draft_id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
