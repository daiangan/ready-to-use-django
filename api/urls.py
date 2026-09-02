from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("openapi/", SpectacularAPIView.as_view(), name="openapi-schema"),
    path(
        "doc/",
        SpectacularSwaggerView.as_view(url_name="openapi-schema"),
        name="swagger-ui",
    ),
]
