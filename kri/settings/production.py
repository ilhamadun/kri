"""Django settings for test server

Make sure to assign coass.settings.test to DJANGO_SETTINGS_MODULE environment variable
before running the test server.
"""

import os
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['kri2017.ugm.ac.id']

ADMINS = [('Ilham Imaduddin', 'ilham.imaduddin@mail.ugm.ac.id')]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static Files and Compression

COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)
COMPRESS_OFFLINE = os.environ.get('COMPRESS_OFFLINE', False)
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter'
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_OUTPUT_DIR = 'cache'

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
