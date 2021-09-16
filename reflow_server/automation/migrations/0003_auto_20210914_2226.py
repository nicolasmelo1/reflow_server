# Generated by Django 3.2.5 on 2021-09-14 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0002_automation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='automationapp',
            name='label_name',
            field=models.CharField(default='New Value', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='automationapp',
            name='logo_url',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='automationappaction',
            name='input_formulary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='automation.automationinputformulary'),
        ),
        migrations.AlterField(
            model_name='automationapptrigger',
            name='input_formulary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='automation.automationinputformulary'),
        ),
        migrations.AlterField(
            model_name='automationapptrigger',
            name='trigger_webhook',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
