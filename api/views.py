from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import CharField


@extend_schema(
    responses={200: inline_serializer("HealthCheck", fields={"status": CharField()})},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Return a lightweight liveness response without touching the database."""
    return Response({"status": "ok"})
