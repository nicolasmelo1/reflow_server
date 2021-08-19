from django.db import models


class AbstractPDFTemplateConfiguration(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)
    rich_text_page = models.ForeignKey('rich_text.TextPage', models.CASCADE, db_index=True, null=True)

    class Meta:
        abstract = True