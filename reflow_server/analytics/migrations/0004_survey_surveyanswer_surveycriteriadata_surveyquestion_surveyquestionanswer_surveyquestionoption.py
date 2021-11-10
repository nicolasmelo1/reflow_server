# Generated by Django 3.2.5 on 2021-11-09 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0003_companyanalytics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.TextField()),
                ('does_display_survey_name', models.BooleanField(default=False)),
                ('criteria_function_name', models.CharField(blank=True, max_length=255, null=True)),
                ('time_in_minutes_for_retaking', models.BigIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'survey',
            },
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_answer_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'survey_answer',
            },
            managers=[
                ('analytics_', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=True)),
                ('question', models.TextField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_questions', to='analytics.survey')),
            ],
            options={
                'db_table': 'survey_question',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question_options', to='analytics.surveyquestion')),
            ],
            options={
                'db_table': 'survey_question_option',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question_answers', to='analytics.surveyanswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_question_answer_questions', to='analytics.surveyquestion')),
            ],
            options={
                'db_table': 'survey_question_answer',
            },
        ),
        migrations.CreateModel(
            name='SurveyCriteriaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_criteria_data', to='analytics.survey')),
            ],
            options={
                'db_table': 'survey_criteria_data',
            },
        ),
    ]
