from .base import *

from .const import *

DEBUG = True

# Укажите True, если отправка email должна вестись асинхронно
STATUS_CELERY = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}
