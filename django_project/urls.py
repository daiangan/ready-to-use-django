from django.conf import settings
from django.contrib import admin
from django.urls import path, include

API_VERSION = settings.API_VERSION

urlpatterns = [
    path(
        'backadmin/',
        admin.site.urls,
    ),
    path(
        f'api/{API_VERSION}/',
        include('api.urls'),
    ),
]
