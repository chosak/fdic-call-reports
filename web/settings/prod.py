import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = '4h=6tp37*3c&92f$y00%!r4+s!l*w*iij07n-cjqk&tuf=%3wa'

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.chosak.org',
]

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

DATABASES = {}

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
        'file': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/wsgi/app.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'error': {
            'level': 'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/wsgi/error.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'reports': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            'cache.kez3tf.cfg.use1.cache.amazonaws.com:11211',
        ]
    }
}
