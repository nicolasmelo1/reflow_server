from django.db import migrations, models
import django.db.models.deletion

def migrate_company_to_company_billing(apps, schema_editor):
    Company = apps.get_model('authentication', 'Company')
    CompanyBilling = apps.get_model('billing', 'CompanyBilling')

    for company in Company.objects.all():
        CompanyBilling.objects.create(
            address=company.address,
            zip_code=company.zip_code,
            street=company.street,
            number=company.number,
            neighborhood=company.neighborhood,
            country=company.country,
            state=company.state,
            city=company.city,
            cnpj=company.cnpj,
            additional_details=company.additional_details,
            is_supercompany=company.is_supercompany,
            is_paying_company=company.is_paying_company,
            vindi_plan_id=company.vindi_plan_id,
            vindi_client_id=company.vindi_client_id,
            vindi_product_id=company.vindi_product_id,
            vindi_payment_profile_id=company.vindi_payment_profile_id,
            company=company,
            payment_method_type=company.payment_method_type,
            charge_frequency_type=company.charge_frequency_type,
            invoice_date_type=company.invoice_date_type
        )
    
class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_companybilling'),
    ]

    operations = [
        migrations.RunPython(migrate_company_to_company_billing)
    ]
