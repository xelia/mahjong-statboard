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


