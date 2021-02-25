from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.kanban.serializers import KanbanFieldsSerializer, KanbanCardsSerializer, KanbanDefaultSerializer, \
    ChangeKanbanCardBetweenDimensionsSerializer, KanbanDimensionSerializer, KanbanCollapsedDimensionSerializer
from reflow_server.kanban.services import KanbanService
from reflow_server.kanban.models import KanbanCard, KanbanDefault, KanbanCollapsedOption


class KanbanFieldsView(APIView):
    """
    This view is responsible for loading the initial and required data to load the kanban,
    kanban visualization has some data saved and that needs to be retrieved by the client in order to load
    the visualization, stuff like what is the default kanban card to be used or what is the default dimension to be used.

    Methods:
        GET: retrieve the initial data needed to load the kanban visualization
    """
    def get(self, request, company_id, form):
        serializer = KanbanFieldsSerializer(user_id=request.user.id, company_id=company_id, form_name=form)
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
        GET: retrieve the kanban cards for a particular formulary.
        POST: saves a new kanban card to be used on this formulary.
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
        PUT: Edits a single kanban_card_id
        DELETE: Deletes a single kanban_card_id
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


class KanbanDefaultView(APIView):
    """
    Responsible for retrieving the defaults of the user for this particular formulary and for this particular company,
    with this we can build the kanban when the user opens the kanban.

    Methods:
        GET: Retrieve the kanban defaults to the user on the first load of the formulary
    """
    def get(self, request, company_id, form):
        instance = KanbanDefault.objects.filter(user=request.user.id, company_id=company_id, form__form_name=form).first()
        serializer = KanbanDefaultSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanEditDefaultView(APIView):
    """
    This view is responsible for saving the default kanban_card_id to be retrieved when the user
    opens the kanban again. So when the user opens the kanban in a particular company and for a particular
    form, the kanban is `automagically` loaded for him.

    Methods:
        PUT: sends the new default ids that are saved to our database.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, form):
        instance = KanbanDefault.objects.filter(user=request.user.id, company_id=company_id, form__form_name=form).first()
        serializer = KanbanDefaultSerializer(data=request.data, instance=instance, context={
            'user_id': request.user.id, 
            'company_id': company_id, 
            'form_name': form
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanDimensionPhaseView(APIView):
    """
    This view is responsible for retrieve each phase of a particular dimension.

    Be aware that each phase of the kanban is actually bounded to the field_option table.

    Methods:
        GET: Retrieves the possible phases of a dimension
     """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form, field_id):
        kanban_service = KanbanService(user_id=request.user.id, company_id=company_id, form_name=form)
        instances = kanban_service.get_dimension_phases(field_id)
        serializer = KanbanDimensionSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanCollapsedDimensionPhasesView(APIView):
    """
    This is for retrieving and for updating the collapsed dimension phase. Collapse dimension phases are dimension phases (or field_options)
    that are not shown to the user when he opens the kanban.
    This is also for saving the collapsed kanban dimensions.

    Methods:
        GET: Retrieve the collapsed dimension phases
        POST: Update the collapsed dimension phases
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form, field_id):
        instances = KanbanCollapsedOption.objects.filter(user_id=request.user.id, company_id=company_id, field_option__field_id=field_id)
        serializer = KanbanCollapsedDimensionSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id, form, field_id):
        instances = KanbanCollapsedOption.objects.filter(user_id=request.user.id, company_id=company_id, field_option__field_id=field_id)
        serializer = KanbanCollapsedDimensionSerializer(data=request.data, instance=instances, many=True, context={
            'user_id': request.user.id, 
            'company_id': company_id, 
            'form_name': form
        })
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok',
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class KanbanChangeDimensionPhasesView(APIView):
    """
    Adds, removes, edit and create new dimension phases (new field_options). In a specific dimension.
    This is basically changing a field_id

    Methods:
        PUT: This is a single method to remove, reorder, edit and create new dimension phases in the kanban. We recieve a list
        here and the ordering is extremely important since that's how we organize the ordering
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, form, field_id):
        kanban_service = KanbanService(user_id=request.user.id, company_id=company_id, form_name=form)
        instances = kanban_service.get_dimension_phases(field_id)
        serializer = KanbanDimensionSerializer(instance=instances, data=request.data, many=True, context={
            'field_id': field_id,
            'user_id': request.user.id,
            'company_id': company_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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