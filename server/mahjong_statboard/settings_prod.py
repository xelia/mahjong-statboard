from .settings import *
from .secret_key import SECRET_KEY


DEBUG = False

ALLOWED_HOSTS = ['rating.tesuji.ru', 'new-rating.tesuji.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mahjong_statboard',
        'HOST': '127.0.0.1',
        'USER': 'mahjong_statboard',
        'PASSWORD': 'mahjong_statboard',
    }
}


STATIC_ROOT = "/var/www/mahjong_statboard/django-static/"
STATIC_URL = '/django-static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'INFO',
            'formatter': 'simple',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/mahjong_statboard/rating.log'
        },
        'player_merge_file': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/mahjong_statboard/player_merge.log'
        },
        'add_games_file': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/mahjong_statboard/add_games.log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'player_merge': {
            'handlers': ['player_merge_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'add_games': {
            'handlers': ['add_games_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
