# Generated by Django 3.0.6 on 2020-06-08 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeFrequencyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'charge_frequency_type',
            },
        ),
        migrations.CreateModel(
            name='ChargeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'charge_type',
            },
        ),
        migrations.CreateModel(
            name='DiscountCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('permanent', models.BooleanField(default=False)),
                ('start_at', models.DateTimeField(default=None, null=True)),
                ('end_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'discount_coupon',
            },
        ),
        migrations.CreateModel(
            name='InvoiceDateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField()),
            ],
            options={
                'db_table': 'invoice_date_type',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'payment_method_type',
            },
        ),
        migrations.CreateModel(
            name='IndividualChargeValueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('default_quantity', models.IntegerField(blank=True, null=True)),
                ('charge_frequency_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.ChargeFrequencyType')),
                ('charge_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.ChargeType')),
            ],
            options={
                'db_table': 'individual_charge_value_type',
            },
        ),
        migrations.CreateModel(
            name='DiscountByIndividualValueQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=250)),
                ('individual_charge_value_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.IndividualChargeValueType')),
            ],
            options={
                'db_table': 'discount_by_individual_value',
            },
        ),
        migrations.CreateModel(
            name='CurrentCompanyCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_company_charges', to='authentication.Company')),
                ('discount_by_individual_value', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.DiscountByIndividualValueQuantity')),
                ('individual_charge_value_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.IndividualChargeValueType')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'current_company_charge',
            },
        ),
        migrations.CreateModel(
            name='CompanyInvoiceMails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_invoice_emails', to='authentication.Company')),
            ],
            options={
                'db_table': 'company_invoice_mails',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CompanyCoupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_discount_coupons', to='authentication.Company')),
                ('discount_coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.DiscountCoupon')),
            ],
            options={
                'db_table': 'company_coupon',
            },
        ),
        migrations.CreateModel(
            name='CompanyCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateTimeField()),
                ('attempt_count', models.IntegerField(default=0)),
                ('charge_date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_charges', to='authentication.Company')),
            ],
            options={
                'db_table': 'company_charge',
            },
        ),
    ]
