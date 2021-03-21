from reflow_server.authentication.managers import public_access
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.serializers.settings import GroupSerializer, FormularySerializer, \
    SectionSerializer, FieldSerializer
from reflow_server.formulary.serializers import PublicAccessFormSerializer
from reflow_server.formulary.models import Group, Form, Field, PublicAccessForm


############################################################################################
class GroupSettingsView(APIView):
    # ------------------------------------------------------------------------------------------
    def get(self, request, company_id):
        instances = Group.objects.filter(company=company_id)
        serializer = GroupSerializer(instance=instances, many=True, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        })
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class GroupEditSettingsView(APIView):
    """
    This view is used for creating or editing groups.

    Methods:
        PUT: edit an existing group
        DELETE: deletes an existing group
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def put(self, request, company_id, group_id):
        instance = Group.objects.filter(company_id=company_id, id=group_id).first()
        serializer = GroupSerializer(instance=instance, data=request.data, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = GroupSerializer(instance=instance, context={
                'company_id': company_id,
                'user_id': request.user.id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------
    def delete(self, request, company_id, group_id):
        instance = Group.objects.filter(id=group_id, company_id=company_id).first()
        if instance:
            instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------

############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class FormularySettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def post(self, request, company_id):
        serializer = FormularySerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = FormularySerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class FormularySettingsEditView(APIView):
    """
    This view is used for editing a single formulary and for loading the formulary contents, 
    with all of it's sections and fields.

    Methods:
        GET: retrieves the data of the formulary containing all of it's sections and fields
        PUT: edit a single formulary data (the section can be omitted)
        DELETE: deletes a single formulary id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def get(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        serializer = FormularySerializer(instance=instance, is_loading_sections=True, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------
    def put(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        serializer = FormularySerializer(instance=instance, data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = FormularySerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'ok',
            'data': None
        }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------
    def delete(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        if instance:
            instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class SectionSettingsView(APIView):
    """
    This view is used for creating a new section instance of a formulary only

    Methods:
        POST: creates a new section instance
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def post(self, request, company_id, form_id):
        serializer = SectionSerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = SectionSerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id,
                'form_id': form_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class SectionSettingsEditView(APIView):
    """
    Edit a section instance, this edition handles the update and the delete of a section

    Methods:
        PUT: updates a section instance
        DELETE: deletes a section instance
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def put(self, request, company_id, form_id, section_id):
        instance = Form.objects.filter(
            id=section_id, 
            depends_on__group__company_id=company_id, 
            depends_on_id=form_id
        ).first()
        serializer = SectionSerializer(instance=instance, data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = SectionSerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id,
                'form_id': form_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------
    def delete(self, request, company_id, form_id, section_id):
        instance = Form.objects.filter(
            id=section_id, 
            depends_on__group__company_id=company_id, 
            depends_on_id=form_id
        ).first()
        if instance:
            instance.delete()
            
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class FieldSettingsView(APIView):
    """
    Creates a new field instance, only.

    Methods:
        POST: Creates a new Field instance
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def post(self, request, company_id, form_id):
        serializer = FieldSerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = FieldSerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id,
                'form_id': form_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class FieldSettingsEditView(APIView):
    """
    Edits a single field instance.

    Methods:
        PUT: Creates a field instance
        DELETE: Deletes a field instance
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def put(self, request, company_id, form_id, field_id):
        instance = Field.objects.filter(
            id=field_id, 
            form__depends_on__group__company_id=company_id, 
            form__depends_on_id=form_id
        ).first()
        serializer = FieldSerializer(instance=instance, data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            instance = serializer.save()
            serializer = FieldSerializer(instance=instance, context={
                'user_id': request.user.id,
                'company_id': company_id,
                'form_id': form_id
            })
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_502_BAD_GATEWAY)
    # ------------------------------------------------------------------------------------------
    def delete(self, request, company_id, form_id, field_id):
        instance = Field.objects.filter(
            id=field_id, 
            form__depends_on__group__company_id=company_id, 
            form__depends_on_id=form_id
        ).first()
        if instance:
            instance.delete()
            
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------


############################################################################################
class FieldOptionsView(APIView):
    """
    View responsible for retrieving all of the fields that can be used in connections.

    Methods:
        GET: Retrieves all of the fields that can be user in connections.
    """
    # ------------------------------------------------------------------------------------------
    def get(self, request, company_id, form_id):
        instances = Field.objects.filter(
                form__depends_on_id=form_id, form__depends_on__group__company_id=company_id
            ).exclude(
                Q(type__type='attachment') | Q(form__type__type__in=['multi-form'])
            )
        serializer = FieldSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        })
    # ------------------------------------------------------------------------------------------


############################################################################################
@method_decorator(csrf_exempt, name='dispatch')
class PublicFormSettingsView(APIView):
    """
    View used for editing and loading the public formulary data, with this we can set the what fields
    are public and which of them are not public.

    Methods:
        GET: Loads the public formulary data, so the user can edit
        POST: Creates a new public formulary.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    # ------------------------------------------------------------------------------------------
    def get(self, request, company_id, form_id):
        instance = PublicAccessForm.objects.filter(public_access__user_id=request.user.id, form_id=form_id).first()
        serializer = PublicAccessFormSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    # ------------------------------------------------------------------------------------------
    def post(self, request, company_id, form_id):
        serializer = PublicAccessFormSerializer(data=request.data)
        if serializer.is_valid():
            public_access_key = serializer.save(form_id, company_id, request.user.id)
            return Response({
            'status': 'ok',
            'data': {
                'public_access_key': public_access_key
            }
        }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
    # ------------------------------------------------------------------------------------------