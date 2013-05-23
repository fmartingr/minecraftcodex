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

# Sentry
RAVEN_CONFIG = {
    'dsn': 'http://809b0824b821462db7902f96cf5ad2c9:bf82b9625be84d9fb2f2a15af1009176@sentry.fmartingr.com/4',
}

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
    'gunicorn'
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}
