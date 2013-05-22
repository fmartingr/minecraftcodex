LOCAL_SETTINGS = True
from settings import *
from os import environ

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': environ['DATABASE_NAME'],
        'USER': environ['DATABASE_USER'],
        'PASSWORD': environ['DATABASE_PASS'],
        'HOST': environ['DATABASE_HOST'],
        'PORT': environ['DATABASE_PORT'],
    }
}

ALLOWED_HOSTS = [
    'minecraftcodex.com',
    'www.minecraftcodex.com',
    'localhost',
    '127.0.0.1',
]

# Staticfiles
STATIC_ROOT = 'static'
STATIC_URL = '/static/'

# Mediafiles
MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
