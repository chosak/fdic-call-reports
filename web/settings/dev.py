import os, socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = '4h=6tp37*3c&92f$y00%!r4+s!l*w*iij07n-cjqk&tuf=%3wa'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'reports',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'reports.urls'
WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'django',
        'HOST': os.environ['DJANGO_RDS_HOST'],
        'USER': os.environ['DJANGO_RDS_USER'],
        'PASSWORD': os.environ['DJANGO_RDS_PASSWORD'],
        'PORT': 3306,
    },  
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'reports': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}

try:
    socket.create_connection(('localhost', 11211))
except socket.error:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': ['localhost:11211',]
        }
    }
