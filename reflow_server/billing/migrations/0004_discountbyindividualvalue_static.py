# Generated by Django 3.0.6 on 2020-08-03 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_individualchargevaluetype_charge_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountbyindividualvalue',
            name='static',
            field=models.BooleanField(default=False),
        ),
    ]
