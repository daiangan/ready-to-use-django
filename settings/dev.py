"""Local development settings."""

from settings.base import *  # noqa: F403

DEBUG = True
MIDDLEWARE.remove("whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
ALLOWED_HOSTS = env_list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,[::1]",
)

# Convenient for separate local frontends. Production always uses an allowlist.
CORS_ALLOW_ALL_ORIGINS = env_bool("DJANGO_CORS_ALLOW_ALL", True)  # noqa: F405

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
