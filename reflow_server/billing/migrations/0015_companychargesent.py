# Generated by Django 3.2.5 on 2021-10-01 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_userextended_timezone_name'),
        ('billing', '0014_remove_currentcompanycharge_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyChargeSent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_charges_sent', to='authentication.company')),
            ],
            options={
                'db_table': 'company_bill_created',
            },
        ),
    ]
