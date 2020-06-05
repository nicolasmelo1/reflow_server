from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.listing.services import ListingService
from reflow_server.listing.serializers import ListingHeaderSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ListingHeader(View):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, form, company_id):
        listing_service = ListingService(user_id=request.user.id, company_id=company_id, form_name=form)
        serializer = ListingHeaderSerializer(
            instance=listing_service.get_listing_selected_fields,
            many=True
        )
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, form, company_id):
        serializer = ListingHeaderSerializer(
            data=request.data,
            many=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_502_BAD_GATEWAY)