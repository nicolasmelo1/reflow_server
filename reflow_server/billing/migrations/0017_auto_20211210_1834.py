# Generated by Django 3.2.5 on 2021-12-10 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0016_billingplan_billingplanpermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingplanpermission',
            name='price_multiplicator',
            field=models.DecimalField(decimal_places=10, default=None, max_digits=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companybilling',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.billingplan'),
        ),
    ]
