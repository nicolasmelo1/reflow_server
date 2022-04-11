"""
Django settings for reflow_server project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

import os
import config
import logging


ENV = os.environ.get('CONFIG', 'development')
if ENV == 'development':
    configuration = config.DevelopmentConfig()
elif ENV == 'server':
    configuration = config.ServerConfig()
else:
    configuration = config.DevelopmentConfig()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create logs directory
if not os.path.exists("{}/logs/".format(BASE_DIR)):
    os.makedirs("{}/logs/".format(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
APP_NAME = os.path.basename(os.path.realpath(os.path.dirname(__file__)))

SECRET_KEY = configuration.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = configuration.DEBUG

ALLOWED_HOSTS = configuration.ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    'channels',
    'rest_framework',
    'reflow_server.analytics',
    'reflow_server.authentication',
    'reflow_server.billing',
    'reflow_server.core',
    'reflow_server.dashboard',
    'reflow_server.data',
    'reflow_server.draft',
    'reflow_server.filter',
    'reflow_server.formula',
    'reflow_server.formulary',
    'reflow_server.notification',
    'reflow_server.notify',
    'reflow_server.kanban',
    'reflow_server.listing',
    'reflow_server.theme',
    'reflow_server.rich_text',
    'reflow_server.pdf_generator',
    'reflow_server.automation',
    'reflow_server.integration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'reflow_server.core.middleware.CORSMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reflow_server.authentication.middleware.AuthJWTMiddleware',
    'reflow_server.authentication.middleware.AuthPublicMiddleware',
]

ROOT_URLCONF = 'reflow_server.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reflow_server.wsgi.application'
ASGI_APPLICATION = 'reflow_server.asgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
DATABASES = configuration.DATABASES
DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'authentication.UserExtended'

AUTHENTICATION_BACKENDS = (
    'reflow_server.authentication.backends.EmailBackend',
)

AUTH_PASSWORD_VALIDATORS = []

# we were getting this error https://stackoverflow.com/questions/41408359/requestdatatoobig-request-body-exceeded-settings-data-upload-max-memory-size
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'console': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '{}/logs/debug.log'.format(BASE_DIR)
        }
    },
    'loggers': {
        'asyncio': {
            'level': 'WARNING',
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Non Default django configutations (Channels, Rest Framework, Cors Headers, etc.)
# https://www.django-rest-framework.org/api-guide/settings/
# https://channels.readthedocs.io/en/latest/tutorial/index.html

# DJANGO CHANNELS CONFIGUTATION
CHANNEL_LAYERS = configuration.CHANNEL_LAYERS

# REST FRAMEWORK CONFIGURATION 
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ]
}


# Reflow configurations, configurations specific for Reflow project

# CUSTOM EVENTS CONFIGURATION
# check reflow_server.core.events file for reference
EVENTS = {
    'user_started_onboarding': {
        'data_parameters': ['visitor_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'user_onboarding': {
        'data_parameters': ['user_id', 'company_id', 'visitor_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'user_login': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.analytics.events.SurveyEvents']
    },
    'user_refresh_token': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.analytics.events.SurveyEvents']
    },
    'user_created': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'user_updated': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.authentication.events.AuthenticationBroadcastEvent']
    },
    'formulary_data_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'form_data_id', 'is_public', 'data'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.data.events.DataBroadcastEvent', 'reflow_server.automation.events.AutomationEvent']
    },
    'formulary_data_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'form_data_id', 'is_public', 'data'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.data.events.DataBroadcastEvent', 'reflow_server.automation.events.AutomationEvent']
    },
    'formulary_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.formulary.events.FormularyBroadcastEvent']
    },
    'formulary_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.formulary.events.FormularyBroadcastEvent']
    },
    'field_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'section_id', 'field_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.formulary.events.FormularyBroadcastEvent']
    },
    'field_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'section_id', 'field_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.formulary.events.FormularyBroadcastEvent']
    },
    'new_paying_company': {
        'data_parameters': ['user_id', 'company_id', 'total_paying_value'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.billing.events.BillingBroadcastEvent']
    },
    'updated_billing_information': {
        'data_parameters': ['user_id', 'company_id', 'total_paying_value'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.billing.events.BillingBroadcastEvent']
    },
    'company_information_updated': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.authentication.events.AuthenticationBroadcastEvent']
    },
    'removed_old_draft': {
        'data_parameters': ['user_id', 'company_id', 'draft_id', 'draft_is_public'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents', 'reflow_server.draft.events.DraftBroadcastEvent']
    },
    'theme_select': {
        'data_parameters': ['user_id', 'company_id', 'theme_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'theme_eyeballing': {
        'data_parameters': ['user_id', 'theme_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'pdf_template_downloaded': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'pdf_template_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'pdf_template_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'pdf_template_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'pdf_template_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'pdf_template_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'kanban_default_settings_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'kanban_card_id', 'kanban_dimension_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'kanban_default_settings_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'kanban_card_id', 'kanban_dimension_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'kanban_loaded': {
        'data_parameters': ['user_id', 'company_id', 'form_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'listing_loaded': {
        'data_parameters': ['user_id', 'company_id', 'form_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'dashboard_loaded': {
        'data_parameters': ['user_id', 'company_id', 'form_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'dashboard_chart_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'dashboard_chart_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'dashboard_chart_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'dashboard_chart_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'notification_loaded': {
        'data_parameters': ['user_id', 'company_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'notification_configuration_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'notification_configuration_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    },
    'notification_configuration_updated': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'notification_configuration_id'],
        'consumers': ['reflow_server.analytics.events.AnalyticsEvents']
    }
}

# CUSTOM DJANGO CHANNELS CONFIGURATION 
# check reflow_server.core.consumers file
CONSUMERS = {
    'LOGIN_REQUIRED': [
        'reflow_server.analytics.consumers.AnalyticsSurveyConsumer',
        'reflow_server.data.consumers.DataConsumer',
        'reflow_server.billing.consumers.BillingConsumer',
        'reflow_server.authentication.consumers.AuthenticationConsumer',
        'reflow_server.draft.consumers.DraftConsumer',
        'reflow_server.formulary.consumers.FormularyConsumer'
    ],
    'PUBLIC': [
        'reflow_server.draft.consumers.DraftPublicConsumer',
    ],
}

# CUSTOM PERMISSIONS CONFIGURATION
# check core.permissions file for reference
PERMISSIONS = {
    'DEFAULT': [
        'reflow_server.authentication.permissions.AuthenticationDefaultPermission',
        'reflow_server.data.permissions.DataDefaultPermission',
        'reflow_server.kanban.permissions.KanbanDefaultPermission',
        'reflow_server.dashboard.permissions.DashboardDefaultPermission',
        'reflow_server.formulary.permissions.FormularyDefaultPermission',
        'reflow_server.notification.permissions.NotificationDefaultPermission',
        'reflow_server.theme.permissions.ThemeDefaultPermission'
    ],
    'PUBLIC': [
        'reflow_server.formulary.permissions.FormularyPublicPermission',
        'reflow_server.authentication.permissions.AuthenticationPublicPermission',
    ],
    'BILLING': [
        'reflow_server.billing.permissions.BillingBillingPermission',
        'reflow_server.draft.permissions.DraftBillingPermission',
        'reflow_server.dashboard.permissions.ChartsBillingPermission',
        'reflow_server.notification.permissions.NotificationBillingPermission',
        'reflow_server.pdf_generator.permissions.PDFGeneratorBillingPermission',
        'reflow_server.formulary.permissions.FormularyBillingPermission',
        'reflow_server.theme.permissions.ThemeBillingPermission'
    ]
}

# CUSTOM FORMULA BUILTIN CONFIGURATION
# check formula.utils.settings for reference
FORMULA_MODULES = {
    'default': [
        'HTTP',
        'SMTP',
        'Reflow',
        'Datetime',
        'List',
        'String',
        'Number',
        'GoogleSheets'
    ],
    'automation': [
        'Automation'
    ]
}

FORMULA_BUILTIN_MODULES_PATH = 'reflow_server.formula.utils.builtins.library'

# CUSTOM ASYNC CONFIGURATION
# check core.utils.asynchronous file
ASYNC_RESPONSE_MAXIMUM_CONCURRENCY_THREADS = 25

# CUSTOM JWT CONFIGURATION
# check authentication.utils.jwt_auth file
JWT_ENCODING = 'HS256'
JWT_HEADER_TYPES = ('Client',)

# FORMULA CONFIGURATION
# check formula.utils.parser file
FORMULA_MAXIMUM_EVAL_TIME = 20

# DATE FIELD CONFIGURATION
# check formulary.models.FieldDateFormatType
"""
Dates are saved in this default format, this way it becomes easier to work with it regardless
the location the user is accessing
"""
DEFAULT_PSQL_DATE_FIELD_FORMAT = 'YYYY-MM-DD HH24:MI:SS'
DEFAULT_DATE_FIELD_FORMAT = '%Y-%m-%d %H:%M:%S'


# NUMBER FIELD CONFIGURATION
# check formulary.models.FieldNumberFormatType
"""
Numbers are saved as `INTEGERs` in our DB since it's very difficult to work
with float values in computing, with this, we define a BASE NUMBER, so every integer saved
is multiplied by it, and every decimal is saved following the rule FLOATNUMBER * (BASE/PRECISION)
"""
DEFAULT_BASE_NUMBER_FIELD_FORMAT = 100000000

# AWS CONFIGURATION
AWS_SECRET_ACCESS_KEY = configuration.AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID = configuration.AWS_ACCESS_KEY_ID

# LOCALSTACK CONFIGURATION
# only needed in development
LOCALSTACK_ENDPOINT = getattr(configuration, 'LOCALSTACK_ENDPOINT', '')
LOCALSTACK_PORT = getattr(configuration, 'LOCALSTACK_PORT', '')

FRONT_END_APP_HOST = 'https://app-beta.reflow.com.br'

# S3 CONFIGURATION
# check core.utils.bucket file
S3_REGION_NAME = configuration.S3_REGION_NAME
S3_FILE_RICH_TEXT_IMAGE_PATH = configuration.S3_FILE_RICH_TEXT_IMAGE_PATH
S3_FILE_DRAFT_PATH = configuration.S3_FILE_DRAFT_PATH
S3_FILE_ATTACHMENTS_PATH = configuration.S3_FILE_ATTACHMENTS_PATH
S3_FILE_DEFAULT_ATTACHMENTS_PATH = configuration.S3_FILE_DEFAULT_ATTACHMENTS_PATH
S3_COMPANY_LOGO_PATH = configuration.S3_COMPANY_LOGO_PATH
S3_USER_PROFILE_IMAGE_PATH = configuration.S3_USER_PROFILE_IMAGE_PATH
S3_BUCKET = configuration.S3_BUCKET

# AUTH BEARER CONFIGURATION (this is the app that we use to authenticate apps on reflow environment)
# check reflow_server.core.decorators and reflow_server.core.services.external
AUTH_BEARER_HOST = configuration.AUTH_BEARER_HOST
AUTH_BEARER_USERNAME = configuration.AUTH_BEARER_USERNAME
AUTH_BEARER_PASSWORD = configuration.AUTH_BEARER_PASSWORD

# EXTERNAL APPS CONFIGURATION
EXTERNAL_APPS = configuration.APPS

# BILLING CONFIGURATION
FREE_TRIAL_DAYS = 15

# VINDI CONFIG
# check reflow_server.billing for explanation, we actually use vindi as our payment gateway on reflow
# so this defines stuff for accessing it's api
VINDI_PRIVATE_API_KEY = configuration.VINDI_PRIVATE_API_KEY
VINDI_PUBLIC_API_KEY = configuration.VINDI_PUBLIC_API_KEY
VINDI_API_HOST = configuration.VINDI_API_HOST
# this one is special, we use it to convert the reflow_server.billing.models.PaymentMethodType to the ones that are
# accepted by vindi. If in our side it is called 'boleto' but vindi accepts only `invoice` we change `boleto` PaymentMethodType.name
# to `invoice`. To use it with environment variables you must set each of them like: 
# VINDI_PAYMENT_METHODS_<the name of the PaymentMethodType> = <The string that vindi accepts>
VINDI_PAYMENT_METHODS = configuration.VINDI_PAYMENT_METHODS
VINDI_WEBHOOK_SECRET_KEY = configuration.VINDI_WEBHOOK_SECRET_KEY
VINDI_ACCEPTED_WEBHOOK_EVENTS = {
    'bill_paid': 'bill',
    'subscription_canceled': 'subscription',
    'subscription_reactivated': 'subscription'
}

FROM_EMAIL = configuration.EMAIL_ADD_NEW_USER

MIXPANEL_TOKEN = configuration.MIXPANEL_TOKEN

if ENV == 'server':
    # SENTRY CONFIGURATION
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )
    sentry_sdk.init(
        environment=ENV,
        dsn=configuration.SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,

        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
    )
