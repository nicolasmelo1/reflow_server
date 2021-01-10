from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.rich_text.services.block import RichTextImageBlockService
from reflow_server.rich_text.serializers import PageSerializer


class RichTextImageView(APIView):
    """
    Class responsible for retrieving the temporary url for the image file saved in
    our storage service. The image is NEVER public, they are always private, because of this we create a url.

    Methods:
        GET - redirects the user to the temporary url of the file.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, page_id, block_uuid, file_name):
        rich_text_image_block_service = RichTextImageBlockService(page_id=page_id, user_id=request.user.id, company_id=company_id)
        url = rich_text_image_block_service.get_image_url(block_uuid, file_name)
        if url != '':
            return redirect(url)
        else:
            return Response({
                'status': 'error'
            })