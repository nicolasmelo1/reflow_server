# Generated by Django 3.1 on 2020-08-28 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20200828_2011'),
        ('billing', '0008_migrate_company_to_company_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybilling',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_company', to='authentication.company'),
        ),
    ]
