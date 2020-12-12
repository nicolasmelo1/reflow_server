from django.db import migrations, models


def migrate_company_to_theme(apps, schema_editor):
    Theme = apps.get_model('theme', 'Theme')
    for theme in Theme.objects.all():
        if hasattr(theme,'company') and theme.user:
            theme.company = theme.user.company
            theme.save()


class Migration(migrations.Migration):
    dependencies = [
        ('theme', '0005_auto_20200929_1701'),
    ]

    operations = [
        migrations.RunPython(migrate_company_to_theme)
    ]