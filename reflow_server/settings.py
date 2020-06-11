"""
Django settings for reflow_server project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import config
try:
    import psycopg2
except ImportError:
    from psycopg2cffi import compat
    compat.register()


ENV = os.environ.get('CONFIG', 'development')
if ENV == 'development':
    configuration = config.DevelopmentConfig()
elif ENV == 'server':
    configuration = config.ServerConfig()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create logs directory
if not os.path.exists("{}/logs/".format(BASE_DIR)):
    os.makedirs("{}/logs/".format(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = configuration.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = configuration.DEBUG

ALLOWED_HOSTS = configuration.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'channels',
    'rest_framework',
    'reflow_server.authentication',
    'reflow_server.billing',
    'reflow_server.core',
    'reflow_server.dashboard',
    'reflow_server.formula',
    'reflow_server.data',
    'reflow_server.formulary',
    'reflow_server.notification',
    'reflow_server.notify',
    'reflow_server.kanban',
    'reflow_server.listing',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'reflow_server.middleware.CORSMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reflow_server.middleware.AuthJWTMiddleware'
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
ASGI_APPLICATION = 'reflow_server.routing.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
DATABASES = configuration.DATABASES


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'authentication.UserExtended'

AUTHENTICATION_BACKENDS = (
    'reflow_server.authentication.backends.EmailBackend',
)

AUTH_PASSWORD_VALIDATORS = []

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
# https://github.com/adamchainz/django-cors-headers

# DJANGO CHANNELS CONFIGUTATION
CHANNEL_LAYERS = configuration.CHANNEL_LAYERS

# REST FRAMEWORK CONFIGURATION 
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ]
}

# CORS HEADERS CONFIGURATION
CORS_EXPOSE_HEADERS=['content-disposition', 'Authorization', '*']
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^\w+://\w+\.reflow\.com$",
    r"^\w+://\w+\.reflow\.com\.br$",
    r"^\w+://localhost:\d+$",
    r"^\w+://127.0.0.1:\d+$",
]

# Reflow configurations, configurations specific for Reflow project

# CUSTOM DJANGO CHANNELS CONFIGURATION 
# check core.consumers file
CONSUMERS = {
    'LOGIN_REQUIRED': [
        'reflow_server.notification.consumers.NotificationReadConsumer'
    ]
}

# CUSTOM ASYNC CONFIGURATION
# check core.utils.asynchronous file
ASYNC_RESPONSE_MAXIMUM_CONCURRENCY_THREADS = 20

# CUSTOM JWT CONFIGURATION
# check authentication.utils.jwt_auth file
JWT_ENCODING = 'HS256'
JWT_HEADER_TYPES = ('Client',)

# FORMULA CONFIGURATION
# check formula.utils.parser file
FORMULA_MAXIMUM_EVAL_TIME = 0.1
FORMULA_FORMULAS = 'reflow_server.formula.utils.formulas'
FORMULA_KEYWORD = 'Formula'
FORMULA_TRIM_SPACES = '_'
FORMULA_TITLE_STRING = True

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
DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION = len(str(DEFAULT_BASE_NUMBER_FIELD_FORMAT))-1

# AWS CONFIGURATION
AWS_SECRET_ACCESS_KEY = configuration.AWS_SECRET_ACCESS_KEY
AWS_ACCESS_KEY_ID = configuration.AWS_ACCESS_KEY_ID

# S3 CONFIGURATION
# check core.utils.bucket file
S3_REGION_NAME = ''
S3_FILE_ATTACHMENTS_PATH = ''
S3_BUCKET = ''

# AUTH BEARER CONFIGURATION (this is the app that we use to authenticate apps on reflow environment)
# check reflow_server.core.decorators and reflow_server.core.services.external
AUTH_BEARER_HOST = configuration.AUTH_BEARER_HOST
AUTH_BEARER_USERNAME = configuration.AUTH_BEARER_USERNAME
AUTH_BEARER_PASSWORD = configuration.AUTH_BEARER_PASSWORD

# EXTERNAL APPS CONFIGURATION
EXTERNAL_APPS = configuration.APPS

# VINDI CONFIG
# check reflow_server.billing for explanation, we actually use vindi as our payment gateway on reflow
# so this defines stuff for accessing it's api
VINDI_PUBLIC_API_KEY = configuration.VINDI_PUBLIC_API_KEY
VINDI_API_HOST = configuration.VINDI_API_HOST
VINDI_PAYMENT_METHODS = configuration.VINDI_PAYMENT_METHODS