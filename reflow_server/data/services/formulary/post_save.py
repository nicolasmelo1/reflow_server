from django.conf import settings
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast

from reflow_server.core.utils.storage import Bucket
from reflow_server.data.services.formulary.data import PostSaveData
from reflow_server.data.models import FormValue, DynamicForm, Attachments
from reflow_server.formulary.models import Field
from reflow_server.formula.services import FormulaService


class PostSave:
    def add_saved_field_value_to_post_process(self, section_instance, form_value_instance):
        if form_value_instance and (form_value_instance.field.type.type in ['id', 'attachment'] or form_value_instance.field.formula_configuration not in ('', None)):
            self.post_save_process.append(PostSaveData(section_instance, form_value_instance))
            return True
        return False

    def post_save(self, formulary_data):
        """
        Cleans certains types of data after it has been saved, it's important to notice it calls `process_fieldtype` function
        so you need to be aware of all the possible field_types in order to create another process function for the correct field_type
        """
        for process in self.post_save_process:
            value = process.form_value_instance.value
            handler = getattr(self, '_post_process_%s' % process.form_value_instance.field.type.type, None)
            if handler:
                process = handler(process)
            
            process = self._post_process_formula(process)
            
            process.form_value_instance.save()

        self.__remove_deleted(formulary_data)
        return None

    def __remove_deleted(self, formulary_data):
        """
        Checks if anything has been deleted, and deletes it.

        Only works if instance is set in the serializer class, since it means you are trying to update a model,
        otherwise, nothing is made and we ignore this function.
        """
        if len(formulary_data.get_sections) != 0 and formulary_data.form_data_id:
            bucket = Bucket()

            section_ids = [section.section_data_id for section in formulary_data.get_sections if section.section_data_id and section.section_data_id != '']
            form_value_ids = [field_value.field_value_data_id for field_value in formulary_data.get_field_values if field_value.field_value_data_id and field_value.field_value_data_id != '']

            fields = Field.objects.filter(form__depends_on__form_name=self.form_name)
            # we do not delete the data of disabled fields
            disabled_fields = fields.filter(Q(enabled=False) | Q(form__enabled=False)).values('id', 'form_id')

            form_value_to_delete = FormValue.objects.filter(
                form__depends_on_id=formulary_data.form_data_id
            ).exclude(
                Q(id__in=form_value_ids) | Q(field_id__in=[disabled_field['id'] for disabled_field in disabled_fields])
            )

            dynamic_forms_to_delete = DynamicForm.objects.filter(
                form__enabled=True, 
                depends_on_id=formulary_data.form_data_id
            ).exclude(id__in=section_ids)
            
            # remove attachments from s3
            for attachment_value in form_value_to_delete.filter(field_type__type='attachment'):
                attachment_to_delete = Attachments.objects.filter(form=attachment_value.form, file=attachment_value.value, field=attachment_value.field).first()
                if attachment_to_delete:
                    bucket.delete(
                        key="{file_attachments_path}/{id}/{field}/{file}".format(
                            id=str(attachment_to_delete.pk),
                            field=str(attachment_to_delete.field.pk),
                            file=str(attachment_to_delete.file),
                            file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
                        )
                    )
                    attachment_to_delete.delete()
            form_value_to_delete.delete()
            dynamic_forms_to_delete.delete()
        return None

    def _post_process_formula(self, process):
        if process.form_value_instance.field.formula_configuration not in ('', None):
            formula = FormulaService(
                process.form_value_instance.field.formula_configuration, 
                precision=process.form_value_instance.field.number_configuration_number_format_type.precision,
                dynamic_form_id=process.section_instance.id
            )
            value = formula.value
            process.form_value_instance.value = value
        return process
    
    def _post_process_id(self, process):
        if process.form_value_instance.value == '0':
            last_id = FormValue.objects.filter(form__form=process.form_value_instance.field.form, field__type=process.form_value_instance.field.type, field=process.form_value_instance.field)\
                .annotate(value_as_int=Cast('value', IntegerField())).order_by('-value_as_int').values_list('value_as_int', flat=True).first()
            value = int(last_id) + 1 if last_id else 1
            process.form_value_instance.value = value
        return process
        
    def _post_process_attachment(self, process):
        if process.form_value_instance.value != '':
            bucket = Bucket()

            dynamic_form_attachment_instance = Attachments.objects.filter(
                file=process.form_value_instance.value,
                field=process.form_value_instance.field,
                form=process.form_value_instance.form
            ).first()

            if not dynamic_form_attachment_instance:
                dynamic_form_attachment_instance = Attachments()
        
            dynamic_form_attachment_instance.file = process.form_value_instance.value
            dynamic_form_attachment_instance.field = process.form_value_instance.field
            dynamic_form_attachment_instance.form = process.form_value_instance.form
            dynamic_form_attachment_instance.save()
            
            print(getattr(self, 'files', {}))
            files = [file_data for file_data in getattr(self, 'files', {}).get(process.form_value_instance.field.name, [])]
            file_data = None
            for file in files:
                if file.name == process.form_value_instance.value:
                    file_data = file
            #handles a simple insertion
            if file_data:
                url = bucket.upload(
                    key="{file_attachments_path}/{id}/{field}/".format(
                        id=str(process.form_value_instance.form.pk), 
                        field=str(process.form_value_instance.field.id), 
                        file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH) + str(process.form_value_instance.value),
                    file=file_data)

                dynamic_form_attachment_instance.file_url = url
                dynamic_form_attachment_instance.file_size = file_data.size
                dynamic_form_attachment_instance.save()
            elif hasattr(self, 'duplicate_form_data_id'):
                to_duplicate = FormValue.objects.filter(form__depends_on=self.duplicate_form_data_id, field_id=process.form_value_instance.field.id, value=str(process.form_value_instance.value)).first()
                if to_duplicate:
                    url = bucket.copy(
                        from_key="{file_attachments_path}/{id}/{field}/".format(
                            id=str(to_duplicate.form.pk), 
                            field=str(to_duplicate.field.id), 
                            file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
                        ) + str(to_duplicate.value),
                        to_key="{file_attachments_path}/{id}/{field}/".format(
                            id=str(process.form_value_instance.form.pk), 
                            field=str(process.form_value_instance.field.id), 
                            file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
                        ) + str(process.form_value_instance.value),
                    )
        return process