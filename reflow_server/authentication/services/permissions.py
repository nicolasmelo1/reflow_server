from django.db.models import Sum, Q

from reflow_server.core.utils import encrypt
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.notification.models import NotificationConfiguration
from reflow_server.kanban.models import KanbanCard
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.formulary.models import Field, Form
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.data.models import DynamicForm, Attachments
from reflow_server.data.services import DataService

import functools


class PermissionService:
    def __init__(self, user_id, company_id, url_name=None, form_name=None, form_id=None, 
                 dynamic_form_id=None, section_id=None, field_id=None,
                 notification_configuration_id=None, kanban_card_id=None):
        self.user = UserExtended.objects.filter(id=user_id).first()
        self.company = Company.objects.filter(id=company_id).first()
        
        if url_name:
            self.url_name = url_name

        if form_id or form_name:
            if form_id:
                self.form = Form.objects.filter(id=form_id, group__company=self.company).first()
            else:
                self.form = Form.objects.filter(form_name=form_name, group__company=self.company).first()

        if notification_configuration_id:
            self.notification_configuration = NotificationConfiguration.objects.filter(user=self.user, id=notification_configuration_id).first()

        if field_id:
            self.field =  Field.objects.filter(id=field_id, form__depends_on__group__company=self.company).first()

        if section_id:
            self.section = Form.objects.filter(id=section_id, depends_on__group__company=self.company).first()
        
        if dynamic_form_id:
            # can maybe be a section so we have to treat it
            self.dynamic_form = DynamicForm.objects.filter(
                Q(id=dynamic_form_id, form__group__company=self.company) | 
                Q(id=dynamic_form_id, form__depends_on__group__company=self.company)
            ).first()

            # if this conditional is set it is probably a section
            if self.dynamic_form and self.dynamic_form.depends_on_id:
                self.dynamic_form = DynamicForm.objects.filter(id=self.dynamic_form.depends_on_id, form__group__company=self.company).first()

        if kanban_card_id:
            self.kanban_card = KanbanCard.objects.filter(id=kanban_card_id, user=self.user).first()

    
    def is_valid_compay(self):
        if self.company.is_active:
            return True
        else:
            return False
    
    def is_valid_user_company(self):
        if self.user.company_id == self.company.id:
            return True
        else:
            return False

    def is_valid_field(self):
        if self.field and self.field.form.depends_on_id in FormularyService(self.user.id, self.company.id).formulary_ids_the_user_has_access_to:
            return True
        else:
            return False

    def is_valid_form(self):
        if self.form and self.form.id in FormularyService(self.user.id, self.company.id).formulary_ids_the_user_has_access_to:
            return True
        else:
            return False

    def is_valid_section(self):
        if self.section and self.section.depends_on_id in FormularyService(self.user.id, self.company.id).formulary_ids_the_user_has_access_to:
            return True
        else:
            return False

    def is_valid_notification_configuration(self):
        return self.notification_configuration != None

    def is_valid_dynamic_form(self):
        if self.dynamic_form and self.form:
            data_service = DataService(self.user.id, self.company.id)
            form_data_ids = data_service.get_user_form_data_ids_from_form_id(self.form.id)
            if int(self.dynamic_form.id) in form_data_ids:
                return True
            else:
                return False
        else:
            return False

    def is_valid_kanban_card(self):
        return self.kanban_card != None

    def is_valid_admin_only_path(self):
        """validates if the user is trying to access an admin only path"""
        from reflow_server.core.utils.routes import admin_only_url_names

        if self.url_name in admin_only_url_names:
            if self.user.profile.name == 'admin':
                return True
            else: 
                return False
        else:
            return True

    def is_valid(self):
        if not self.is_valid_compay():
            return False

        if not self.is_valid_user_company():
            return False

        if hasattr(self, 'url_name'):
            if not self.is_valid_admin_only_path():
                return False

        if hasattr(self, 'form'):
            if not self.is_valid_form():
                return False
        
        if hasattr(self, 'notification_configuration'):
            if not self.is_valid_notification_configuration():
                return False
        
        if hasattr(self, 'field'):
            if not self.is_valid_field():
                return False
        
        if hasattr(self, 'section'):
            if not self.is_valid_section():
                return False

        if hasattr(self, 'dynamic_form'):
            if not self.is_valid_dynamic_form():
                return False
        
        if hasattr(self, 'kanban_card'):
            if not self.is_valid_kanban_card():
                return False
        
        return True
