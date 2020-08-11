from rest_framework import status

from reflow_server.formulary.services.permissions import FormularyPermissionsService
from reflow_server.formulary.models import Field, Form
from reflow_server.core.permissions import PermissionsError


class FormularyDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, section_id=None, field_id=None, form_id=None):
        self.company_id = company_id
        self.form_id = form_id
        self.field_id = field_id
        self.section_id = section_id

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

        if self.form_id and not FormularyPermissionsService.is_valid_form(request.request.user.id, self.company_id, self.form_id):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)
