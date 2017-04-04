"""Django settings for test server

Make sure to assign coass.settings.test to DJANGO_SETTINGS_MODULE environment variable
before running the test server.
"""

import os
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_x+^^i0nd&ynzu(%^hxirc(^sejnt%=(6g7bo-q&vaneg@4&f1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', ""),
        'USER': os.environ.get('DB_USER', ""),
        'PASSWORD': os.environ.get('DB_PASSWORD', ""),
        'HOST': 'localhost',
        'PORT': '',
    }
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
