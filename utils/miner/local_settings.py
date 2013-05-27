LOCAL_SETTINGS = True
from herobrine.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../../dev_ddbb.sqlite',
    }
}

TEMPLATE_CONTEXT = [
    ('app_version', '[local development]'),
]
