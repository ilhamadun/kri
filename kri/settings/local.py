"""Django settings for local development server

Make sure to assign coass.settings.local to DJANGO_SETTINGS_MODULE environment variable
before running the development server.
"""

import os
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_x+^^i0nd&ynzu(%^hxirc(^sejnt%=(6g7bo-q&vaneg@4&f1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
