from .base import *
from decouple import config

APP_URL = "<APP URL HERE>"
HOST_URL = "<HOST URL HERE>"

DEBUG = False

ALLOWED_HOSTS = [
    '<ALLOWED HOSTS HERE>'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
    }
}

CORS_ALLOWED_ORIGINS = [
    '<CORS URLS HERE>',
]

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
