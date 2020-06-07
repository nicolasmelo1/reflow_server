class PostSave:
    def __remove_deleted(self, cleaned_data):
        """
        Checks if anything has been deleted, and deletes it.

        Only works if instance is set in the serializer class, since it means you are trying to update a model,
        otherwise, nothing is made and we ignore this function.
        """
        if len(cleaned_data.get_sections) != 0 and self.__instance:
            bucket = Bucket()

            section_ids = [section.section_data_id for section in cleaned_data.get_sections if section.section_data_id and section.section_data_id != '']
            form_value_ids = [field_value.field_value_data_id for field_value in cleaned_data.get_field_values if field_value.field_value_data_id and field_value.field_value_data_id != '']
            
            fields = Field.objects.filter(form__depends_on__form_name=self.form_name)
            disabled_fields = fields.filter(Q(enabled=False) | Q(form__enabled=False)).values('id', 'form_id')

            form_value_to_delete = FormValue.objects.filter(
                form__depends_on=self.__instance
            ).exclude(
                Q(id__in=form_value_ids) | Q(field_id__in=[disabled_field['id'] for disabled_field in disabled_fields])
            )
            dynamic_forms_to_delete = DynamicForm.objects.filter(
                form__enabled=True, 
                depends_on=self.__instance
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
