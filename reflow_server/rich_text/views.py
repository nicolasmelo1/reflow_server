from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.rich_text.services.block import RichTextImageBlockService
from reflow_server.rich_text.serializers import PageSerializer, TextBlockTypeCanContainTypeSerializer
from reflow_server.rich_text.models import TextBlockTypeCanContainType


class RichTextBlockCanContainBlockView(APIView):
    """
    Retrieves all of the block types another block can contain. Like tables, lists and others that have children blocks.

    Methods:
        GET - Returns a list of block_ids another blocks can contain
    """
    def get(self, request):
        instance = TextBlockTypeCanContainType.rich_text_.all_block_type_can_contain_types()
        serializer = TextBlockTypeCanContainTypeSerializer(instance=instance, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class RichTextImageView(APIView):
    """
    Class responsible for retrieving the temporary url for the image file saved in
    our storage service. The image is NEVER public, they are always private, because of this we create a url.

    Methods:
        GET - redirects the user to the temporary url of the file.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, page_id, file_image_uuid):
        rich_text_image_block_service = RichTextImageBlockService(page_id=page_id, user_id=request.user.id, company_id=company_id)
        url = rich_text_image_block_service.get_image_url(file_image_uuid)
        if url != '':
            return redirect(url)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
