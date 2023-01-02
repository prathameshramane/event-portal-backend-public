from .base import *
from decouple import config

APP_URL = "http://localhost:3000"
HOST_URL = "http://127.0.0.1:8000"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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
    'http://localhost:3000',
]

# Email Credentials
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
