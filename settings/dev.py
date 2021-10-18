from settings.base import *
from settings import databases

DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DATABASES = databases.DEV




