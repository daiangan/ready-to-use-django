"""Production settings with secure defaults."""

import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from settings.base import *  # noqa: F403


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise ImproperlyConfigured(f"The {name} environment variable is required.")
    return value


SECRET_KEY = required_env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")  # noqa: F405
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must contain at least one host.")
DATABASES = {
    "default": dj_database_url.parse(
        required_env("DATABASE_URL"),
        conn_max_age=60,
        conn_health_checks=True,
    )
}

# Only trust X-Forwarded-Proto when the deployment has a trusted reverse proxy that
# strips values supplied by clients and sets the header itself.
if env_bool("DJANGO_TRUST_X_FORWARDED_PROTO", False):  # noqa: F405
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(  # noqa: F405
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)  # noqa: F405

STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}

if os.getenv("AWS_STORAGE_BUCKET_NAME"):
    STORAGES["default"] = {  # noqa: F405
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ["AWS_STORAGE_BUCKET_NAME"],
            "region_name": os.getenv("AWS_S3_REGION_NAME"),
            "custom_domain": os.getenv("AWS_S3_CUSTOM_DOMAIN"),
            "default_acl": None,
            "querystring_auth": env_bool("AWS_QUERYSTRING_AUTH", True),  # noqa: F405
        },
    }
