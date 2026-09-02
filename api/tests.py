from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token


class ApiRouteTests(SimpleTestCase):
    def test_health_check_is_public(self):
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_openapi_schema_is_available(self):
        response = self.client.get(reverse("openapi-schema"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("application/vnd.oai.openapi", response.headers["Content-Type"])

    def test_swagger_ui_is_available(self):
        response = self.client.get(reverse("swagger-ui"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "swagger-ui")


class ApiTokenCommandTests(TestCase):
    def test_command_creates_missing_user_token(self):
        user = get_user_model().objects.create_user(username="test-user")
        output = StringIO()

        call_command("api_tests", stdout=output)

        self.assertTrue(Token.objects.filter(user=user).exists())
        self.assertIn("created", output.getvalue())
