from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [

    # Swagger Documentation
    path('openapi/', get_schema_view(
        title="Project API",
        description="API documentation",
        version=settings.API_VERSION,
    ), name='openapi-schema'),
    path('doc/', TemplateView.as_view(
        template_name='api/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
