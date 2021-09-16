from django.conf import settings

from reflow_server.core.utils.storage import Bucket, BucketUploadException
from reflow_server.data.services.formulary.data import PostSaveData
from reflow_server.data.models import FormValue, DynamicForm, Attachments
from reflow_server.formula.services.formula import FlowFormulaService
from reflow_server.data.services.attachments import AttachmentService

import json


class PostSave:
    def add_saved_field_value_to_post_process(self, section_instance, form_value_instance):
        if form_value_instance and form_value_instance.field.type.type in ['id', 'attachment', 'long_text', 'formula']:
            self.post_save_process.append(PostSaveData(section_instance, form_value_instance))
            return True
        return False

    def post_save(self, formulary_data):
        """
        Cleans certains types of data after it has been saved, it's important to notice it calls `process_fieldtype` function
        so you need to be aware of all the possible field_types in order to create another process function for the correct field_type
        """
        # we need to remove deleted first because of the formulas, on the front-end when we change the value of a field
        # we are actually creating a new FormValue instance. This means that for a short amount of time there will be 2
        # FormValues,one is the newly created instance, the other is the old instance to remove, this two instances can cause some
        # weird behaviour and bugs when calculating formulas
        self.__remove_deleted(formulary_data)

        for process in self.post_save_process:
            handler = getattr(self, '_post_process_%s' % process.form_value_instance.field.type.type, None)
            if handler:
                process = handler(process)
                            
            process.form_value_instance.save()
        return None

    def __remove_deleted(self, formulary_data):
        """
        Checks if anything has been deleted, and deletes it.

        Only works if instance is set in the serializer class, since it means you are trying to update a model,
        otherwise, nothing is made and we ignore this function.

        It's important to understand that we only remove enabled fields, removed fields are ignored, so if you disabled
        a field, the FormValue that it contains will be preserved.
        """
        if len(formulary_data.get_sections) != 0 and formulary_data.form_data_id:
            bucket = Bucket()

            section_ids = [section.section_data_id for section in formulary_data.get_sections if section.section_data_id and section.section_data_id != '']
            form_value_ids = [field_value.field_value_data_id for field_value in formulary_data.get_field_values if field_value.field_value_data_id and field_value.field_value_data_id != '']

            # remove attachments from s3
            for attachment_value in FormValue.data_.attachment_form_values_by_main_form_id_excluding_form_value_ids_and_disabled_fields(formulary_data.form_data_id, form_value_ids):
                attachment_to_delete = Attachments.data_.attachment_by_dynamic_form_id_field_id_and_file_name(attachment_value.form.id, attachment_value.field.id, attachment_value.value)
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
            FormValue.data_.delete_form_values_by_main_form_id_excluding_form_value_ids_disabled_fields_and_conditional_excludes_if_not_set(
                dynamic_form_id=formulary_data.form_data_id, 
                form_value_ids=form_value_ids
            )
            DynamicForm.data_.remove_dynamic_forms_from_enabled_forms_and_by_depends_on_id_and_conditional_excludes_data_if_not_setexcluding_dynamic_form_ids(
                formulary_data.form_data_id,
                section_ids
            )
        return None

    def _post_process_formula(self, process):
        if process.form_value_instance.field.formula_configuration not in ('', None):
            
            formula = FlowFormulaService(
                process.form_value_instance.field.formula_configuration,
                self.user_id,
                self.company_id, 
                formula_context='formula',
                dynamic_form_id=process.section_instance.depends_on.id,
                field_id=process.form_value_instance.field_id
            )
            formula_result = formula.evaluate_to_internal_value()
            value = formula_result.value

            process.form_value_instance.field_type = formula_result.field_type
            process.form_value_instance.number_configuration_number_format_type = formula_result.number_format_type
            process.form_value_instance.date_configuration_date_format_type = formula_result.date_format_type
            process.form_value_instance.value = str(value)
        return process

    def _post_process_id(self, process):
        if process.form_value_instance.value == '0':
            last_id = FormValue.data_.last_saved_value_of_id_field_type(process.form_value_instance.field.form.id, process.form_value_instance.field.type.id, process.form_value_instance.field.id)
            value = int(last_id) + 1 if last_id else 1
            process.form_value_instance.value = value
        return process
        
    def _post_process_attachment(self, process):
        if process.form_value_instance.value != '':
            attachment_service = AttachmentService(user_id=self.user_id, company_id=self.company_id)
            
            attachment_instance = attachment_service.save_attachment(
                process.form_value_instance.form.id, 
                process.form_value_instance.field.id, 
                process.form_value_instance.value
            )

            if hasattr(self, 'duplicate_form_data_id'):
                attachment_instance = attachment_service.duplicate_attachment(
                    attachment_instance,
                    self.duplicate_form_data_id,
                    process.form_value_instance.field.id, 
                    process.form_value_instance.value,
                    process.form_value_instance.form.id,
                    process.form_value_instance.field.id
                )
                if attachment_instance == None:
                    raise BucketUploadException(json.dumps({
                        'detail': [process.form_value_instance.field.name], 
                        'reason': ['could_not_upload'], 
                        'data': [process.form_value_instance.value]
                    }))
            if attachment_instance.file_url in [None, '']:
                raise BucketUploadException(json.dumps({
                    'detail': [process.form_value_instance.field.name], 
                    'reason': ['could_not_upload'], 
                    'data': [process.form_value_instance.value]
                }))

            process.form_value_instance.value = attachment_instance.file
            process.form_value_instance.save()
        return process