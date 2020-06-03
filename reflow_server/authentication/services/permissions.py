from django.db.models import Sum
from reflow_server.core.utils import encrypt
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.notification.models import NotificationConfiguration
from reflow_server.visualization.models import KanbanCard
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.formulary.models import Field, FormAccessedBy, Form, Attachments, DynamicForm
from reflow_server.formulary.services.data import DataService
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
            self.dynamic_form = DynamicForm.objects.filter(id=dynamic_form_id, form__depends_on__group__company=self.company).first()

            # not a section
            if self.dynamic_form.depends_on_id:
                self.dynamic_form = DynamicForm.objects.filter(depends_on_id=self.dynamic_form.id, form__depends_on__group__company=self.company).first()

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
        if self.field and FormAccessedBy.objects.filter(form_id=self.field.form.depends_on_id, user=self.user).exists():
            return True
        else:
            return False

    def is_valid_form(self):
        if FormAccessedBy.objects.filter(form=self.form, user=self.user).exists():
            return True
        else:
            return False

    def is_valid_section(self):
        if self.section and FormAccessedBy.objects.filter(form_id=self.section.depends_on_id, user=self.user).exists():
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
        '''validates if the user is trying to access an admin only path'''
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
    '''
    def is_valid_file(self, url_name, request_files):
        """validates the billing"""
        # TODO: move to billing

        from reflow_server.core.utils.routes import attachment_url_names

        if url_name in attachment_url_names:
            company_aggregated_file_sizes = Attachments.objects.filter(form__user__company=self.company).aggregate(Sum('file_size')).get('file_size__sum', 0)
            current_gb_permission_for_company = CurrentCompanyCharge.objects.filter(individual_charge_value_type__name='per_gb', company=self.company).values_list('quantity', flat=True).first()

            new_files_size = functools.reduce(
                lambda x, y: x + y, [
                    file_data.size for key in request_files.keys() for file_data in request_files.getlist(key)
                ], 0
            ) * 0.000000001
            company_aggregated_file_sizes = company_aggregated_file_sizes if company_aggregated_file_sizes else 0
            company_aggregated_file_sizes = company_aggregated_file_sizes * 0.000000001
            all_file_sizes = new_files_size + company_aggregated_file_sizes

            if all_file_sizes < current_gb_permission_for_company:
                return True
            else:
                return False
        else:
            return True
    '''