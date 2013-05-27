LOCAL_SETTINGS = True
from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev_ddbb.sqlite',
    }
}

TEMPLATE_CONTEXT = [
    ('app_version', '[local development]'),
]
