from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.kanban.serializers import GetKanbanSerializer, KanbanCardsSerializer, KanbanDefaultsSerializer, \
    KanbanDimensionOrderSerializer, ChangeKanbanCardBetweenDimensionsSerializer
from reflow_server.kanban.services import KanbanService
from reflow_server.kanban.models import KanbanCard, KanbanDimensionOrder


class GetKanbanView(APIView):
    """
    This view is responsible for loading the initial and required data to load the kanban,
    kanban visualization has some data saved and that needs to be retrieved by the client in order to load
    the visualization, stuff like what is the default kanban card to be used or what is the default dimension to be used.

    Methods:
        .get() -- retrieve the initial data needed to load the kanban visualization
    """
    def get(self, request, company_id, form):
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

    def get(self, request, company_id, form):
        kanban_service = KanbanService(user_id=request.user.id, company_id=company_id, form_name=form)
        serializer = KanbanCardsSerializer(instance=kanban_service.get_kanban_cards, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id, form):
        serializer = KanbanCardsSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user_id=request.user.id, company_id=company_id, form_name=form)
            serializer = KanbanCardsSerializer(instance=instance)
            return Response({
                'status': 'ok',
                'data': serializer.data
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

    def put(self, request, company_id, form, kanban_card_id):
        instance = KanbanCard.objects.filter(id=kanban_card_id).first()
        serializer = KanbanCardsSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save(user_id=request.user.id, company_id=company_id, form_name=form)
            serializer = KanbanCardsSerializer(instance=instance)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)
    
    def delete(self, request, company_id, form, kanban_card_id):
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

    def put(self, request, company_id, form):
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
class KanbanDimensionOrderView(APIView):
    """
    This view is responsible for two things:

    1 - retrieve the dimension orders
    2 - reorder the dimension of the kanban

    It is actually more complicated than that so let me go for each one. First number 1. Dimension orders are nothing more than
    the options of `option` `field_type` and options of `form` `field_type`. It's as simple as that but this is where things gets
    complicated.
    Dimension orders are NOT bound to the field_options itself, but instead it's stored on a completely different table in our database.
    So we actually don't have direct control when the user changed a option or if he deleted a option in this field of the formulary.
    With this, we only know the options have changed when we load the kanban again and get the options again. And that is EXACTLY what we do, 
    we update the DimensionOrder when retrieving the data.

    Okay so this leaves us if the second point, and that one is easy: the user can reorder the options of the kanban, and when he does
    this we don't need to create or update any dimension, we just reorder with the options that are available for him.

    Methods:
        .get() -- handles the point number 1
        .put() -- handles the point number 2
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form, field_id):
        kanban_service = KanbanService(user_id=request.user.id, company_id=company_id, form_name=form)
        kanban_dimension_orders = kanban_service.get_create_or_update_kanban_dimension_order(field_id)
        serializer = KanbanDimensionOrderSerializer(kanban_dimension_orders, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, company_id, form, field_id):
        instance = KanbanDimensionOrder.objects.filter(dimension_id=field_id, user_id=request.user.id)
        serializer = KanbanDimensionOrderSerializer(data=request.data, instance=instance, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'            
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class ChangeKanbanCardBetweenDimensionsView(APIView):
    """
    This view is responsible to handle when the user changes the dimension of a card in the kanban. It's important to understand how this work.
    If you go to the serializer of this view you will notice that this serializer actually calls the FormularySerilizer in the `formulary` app.
    We use this to don't rewrite the code. So the code works this way:
    - We get a data that tells us the form_value_id to change and the new value, we get the serializer, change the data in the serializer and saves it again.
    if a error is fired we return this error to the user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, form, company_id):
        serializer = ChangeKanbanCardBetweenDimensionsSerializer(
            user_id=request.user.id, 
            form_name=form, 
            company_id=company_id,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)