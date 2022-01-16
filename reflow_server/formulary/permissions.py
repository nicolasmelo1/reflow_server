from rest_framework import status

from reflow_server.formulary.services.permissions import FormularyPermissionsService
from reflow_server.formulary.models import Field, Form, PublicAccessField, PublicAccessForm
from reflow_server.core.permissions import PermissionsError, PublicPermissionIsValidError

############################################################################################
class FormularyDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, section_id=None, field_id=None, form_id=None, form=None):
        self.company_id = company_id
        self.form_id = form_id
        self.field_id = field_id
        self.section_id = section_id
        self.form_name = form
    # ------------------------------------------------------------------------------------------
    def __call__(self, request):
        if self.field_id:
            field = Field.objects.filter(id=self.field_id, form__depends_on__group__company_id=self.company_id).first()
            if not field:
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)

            self.form_id = field.form.depends_on_id

        if self.section_id:
            section = Form.objects.filter(id=self.section_id, depends_on__group__company_id=self.company_id).first()
            if not section:
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)

            self.form_id = section.depends_on_id

        if (self.form_id or self.form_name) and not FormularyPermissionsService.is_valid_form(request.request.user.id, self.company_id, self.form_id, self.form_name):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)
    # ------------------------------------------------------------------------------------------

############################################################################################
class FormularyPublicPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.

    This is for validating if a non authenticated user can access some private contents. This is for loading
    the formulary to the user and mounting on screen for the non authenticated user.
    """
    def __init__(self, company_id=None, field_id=None, form=None):
        self.company_id = company_id
        self.field_id = field_id
        self.form_name = form
    # ------------------------------------------------------------------------------------------
    def __call__(self, request):
        FormularyDefaultPermission(self.company_id, None, self.field_id, None, self.form_name)(request=request)
        # validate public access
        if self.form_name:
            if not self.field_id and PublicAccessForm.formulary_.public_access_form_by_public_access_key_company_id_and_main_form_name(request.public_access_key, self.company_id, self.form_name):
                raise PublicPermissionIsValidError(detail='valid')
            if self.field_id and PublicAccessField.formulary_.exists_field_id_by_public_access_key_and_form_name(request.public_access_key, self.field_id, self.form_name):
                raise PublicPermissionIsValidError(detail='valid')
            else:
                raise PermissionsError(detail='not_permitted')
    # ------------------------------------------------------------------------------------------
############################################################################################
class FormularyBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id):
        self.company_id = company_id
    
    def __call__(self, request):
        if request.url_name == 'formulary_settings_forms' and request.method == 'POST':
            if not FormularyPermissionsService.can_add_new_formulary(self.company_id):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
