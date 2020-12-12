from django.db.models import Q

from rest_framework import status

from reflow_server.data.services.permissions import DataPermissionsService
from reflow_server.formulary.models import Form
from reflow_server.data.models import DynamicForm
from reflow_server.core.permissions import PermissionsError


class DataDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, dynamic_form_id=None, form=None):
        self.company_id = company_id
        self.form = form
        self.dynamic_form_id = dynamic_form_id
    
    def __call__(self, request):
        if self.dynamic_form_id and self.form:
            form = Form.objects.filter(form_name=self.form, group__company_id=self.company_id).first()

            # can maybe be a section so we have to treat it
            dynamic_form = DynamicForm.data_.dynamic_form_by_dynamic_form_id_and_company_id(
                self.dynamic_form_id,
                self.company_id,
                self.form
            )
            # if this conditional is set it is probably a section
            if dynamic_form and dynamic_form.depends_on_id:
                dynamic_form = DynamicForm.data_.dynamic_form_by_dynamic_form_id_and_company_id(
                    dynamic_form.depends_on_id,
                    self.company_id,
                    self.form
                )
            if dynamic_form and form:
                if not DataPermissionsService.is_valid(request.request.user.id, self.company_id, form.id, dynamic_form.id):
                    raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)
            else:
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)


class FileBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None):
        self.company_id = company_id

    def __call__(self, request):
        from reflow_server.data.services.routes import attachment_url_names

        if request.url_name in attachment_url_names and request.method in ['PUT', 'POST']:
            if not DataPermissionsService.is_valid_file_upload(self.company_id, request.files):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
            