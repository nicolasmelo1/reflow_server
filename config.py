import os
import json
import boto3
import requests
import time

config_file = json.loads(open('reflow-config.json').read())

class Config:
    EXTERNAL_APPS = ['reflow_worker', 'reflow_front', 'reflow_billing']


class DevelopmentConfig(Config):
    SECRET_KEY = config_file['secret_key']
    ALLOWED_HOSTS = ['*']
    DEBUG = config_file['debug']

    SECURE_URL = False

    AUTH_BEARER_HOST = config_file['auth_bearer']['host']
    AUTH_BEARER_USERNAME = config_file['auth_bearer']['username']
    AUTH_BEARER_PASSWORD = config_file['auth_bearer']['password']

    VINDI_PUBLIC_API_KEY =  config_file['vindi']['public_api_key']
    VINDI_API_HOST = config_file['vindi']['host']
    VINDI_PAYMENT_METHODS = config_file['vindi']['payment_methods']
    EMAIL_ADD_NEW_USER = config_file['email']['emails']['add_new_user']['email']


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config_file['databases']['name'],
            'USER': config_file['databases']['user'],
            'PASSWORD': config_file['databases']['password'],
            'HOST': config_file['databases']['host'],
            'PORT': config_file['databases']['port']
        },
        'sqlite3': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3'
        }
    }

    LOCALSTACK_ENDPOINT = config_file['aws']['localstack']['endpoint']
    LOCALSTACK_PORT = config_file['aws']['localstack']['port']

    AWS_SECRET_ACCESS_KEY = config_file['aws']['secret_key']
    AWS_ACCESS_KEY_ID = config_file['aws']['access_key']

    S3_REGION_NAME = config_file['aws']['s3_region_name']
    S3_FILE_ATTACHMENTS_PATH = config_file['aws']['s3_file_attachments_path']
    S3_BUCKET = config_file['aws']['s3_bucket']

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': config_file['channels']['backend'],
            'CONFIG': {
                'hosts': [(config_file['channels']['host'], config_file['channels']['port'])],
            },
        }
    }

    APPS = {}

    def __init__(self):
        for app in self.EXTERNAL_APPS:
            self.APPS[app] = config_file['apps'][app]
        
        case = 'error'
        while case == 'error':
            try:
                s3 = boto3.client('s3', endpoint_url="http://localstack:4572",
                                  use_ssl=False, aws_access_key_id='foo', aws_secret_access_key='bar')
                s3.create_bucket(Bucket=self.S3_BUCKET)
                case = 'success'
            except:
                time.sleep(10)


class ServerConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    ALLOWED_HOSTS = ['*']
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'

    SECURE_URL = os.environ.get('SECURE_URL', 'False') == 'True'

    AUTH_BEARER_HOST = os.environ.get('AUTH_BEARER_HOST', '')
    AUTH_BEARER_USERNAME = os.environ.get('AUTH_BEARER_USERNAME', '')
    AUTH_BEARER_PASSWORD = os.environ.get('AUTH_BEARER_PASSWORD', '')

    VINDI_PUBLIC_API_KEY = os.environ.get('VINDI_PUBLIC_API_KEY', '')
    VINDI_API_HOST = os.environ.get('VINDI_API_HOST', '')
    VINDI_PAYMENT_METHODS = dict()

    EMAIL_ADD_NEW_USER = os.environ.get('EMAIL_ADD_NEW_USER', None)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DATABASE_NAME', None),
            'USER': os.environ.get('DATABASE_USER', None),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', None),
            'HOST': os.environ.get('DATABASE_HOST', None),
            'PORT': os.environ.get('DATABASE_PORT', None)
        }
    }

    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)


    S3_REGION_NAME = os.environ.get('S3_REGION_NAME', None)
    S3_FILE_ATTACHMENTS_PATH = os.environ.get('S3_FILE_ATTACHMENTS_PATH', None)
    S3_BUCKET = os.environ.get('S3_BUCKET', None)

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_rabbitmq.core.RabbitmqChannelLayer',
            'CONFIG': {
                'host': os.environ.get('CHANNEL_RABBITMQ_HOST', None),
            },
        }
    }

    APPS = {}

    def __init__(self):
        for key, value in os.environ.items():
            if 'VINDI_PAYMENT_METHODS_' in key:
                self.VINDI_PAYMENT_METHODS[key.replace('VINDI_PAYMENT_METHODS_', '').lower()] = value

        for app in self.EXTERNAL_APPS:
            if self.AUTH_BEARER_HOST != '':
                try:
                    response = requests.post(self.AUTH_BEARER_HOST + '/auth/', json={
                        'username': self.AUTH_BEARER_USERNAME,
                        'password': self.AUTH_BEARER_PASSWORD
                    })
                    header = {"Authorization": "Bearer {}".format(response.json()['access_token'])}
                    response = requests.get(self.AUTH_BEARER_HOST + '/hosts/', headers=header, params={
                        'app': app
                    })
                    if 'url' in response.json():
                        self.APPS[app] = response.json()['url']
                except:
                    continue
