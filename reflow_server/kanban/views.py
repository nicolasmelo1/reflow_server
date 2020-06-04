from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.kanban.serializers import GetKanbanSerializer, KanbanCardsSerializer, KanbanDefaultsSerializer
from reflow_server.kanban.services import KanbanService
from reflow_server.kanban.models import KanbanCard


class GetKanbanView(APIView):
    """
    This view is responsible for loading the initial and required data to load the kanban,
    kanban visualization has some data saved and that needs to be retrieved by the client in order to load
    the visualization, stuff like what is the default kanban card to be used or what is the default dimension to be used.

    Methods:
        .get() -- retrieve the initial data needed to load the kanban visualization
    """
    def get(self, request, form, company_id):
        serializer = GetKanbanSerializer(user_id=request.user.id, company_id=company_id, form_name=form)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanCardsView(APIView):
    """
    This view handles get and post request for retrieve kanban cards, these kanban cards are the cards to build the kanban, 
    not the actual data that is displayed to the user.

    It's important to notice that get returns a list of kanban cards and the other requests expect just one.
    
    Methods:
        .get() -- retrieve the kanban cards for a particular formulary.
        .post() -- saves a new kanban card to be used on this formulary.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, form, company_id):
        kanban_service = KanbanService(user_id=request.user.id, company_id=company_id, form_name=form)
        serializer = KanbanCardsSerializer(instance=kanban_service.get_kanban_cards, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, form, company_id):
        serializer = KanbanCardsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanCardsEditView(APIView):
    """
    This view handles the edition of a single kanban_card_id, most likely KanbanCardsView.

    Methods:
        .put() -- Edits a single kanban_card_id
        .delete() -- Deletes a single kanban_card_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, form, company_id, kanban_card_id):
        instance = KanbanCard.objects.filter(id=kanban_card_id).first()
        serializer = KanbanCardsSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save(user_id=request.user.id)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)
    
    def delete(self, request, form, company_id, kanban_card_id):
        kanban_card = KanbanCard.objects.filter(id=kanban_card_id, user=request.user).first()
        if kanban_card:
            kanban_card.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanSetDefaultsView(APIView):
    """
    This view is responsible for saving the default kanban_card_id to be retrieved when the user
    opens the kanban again. So when the user opens the kanban in a particular company and for a particular
    form, the kanban is `automagically` loaded for him.

    Methods:
        .put() -- sends the new default ids that are saved to our database.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, form, company_id):
        serializer = KanbanDefaultsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user.id, company_id, form)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class APIKanbanDimensionsOrder(View):
    def get(self, request, form, company_id, field_id):
        dimension_orders = get_create_or_update_kanban_dimension_order(encrypt.decrypt_pk(company_id), request.user, field, form)
        serializer = KanbanDimensionOrderSerializer(dimension_orders, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        })
    

    def put(self, request, form, company_id, field_id):
        dimension_orders = KanbanDimensionOrder.objects.filter(dimension_id=field_id, user=request.user)\
            .order_by('order')
        serializer = KanbanDimensionOrderSerializer(data=data, instance=dimension_orders, many=True)

        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        })