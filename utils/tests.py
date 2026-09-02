from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework.authtoken.models import TokenProxy
from unfold.admin import ModelAdmin

from utils.models import TimeStampedModel


class TimeStampedModelTests(SimpleTestCase):
    def test_model_is_abstract(self):
        self.assertTrue(TimeStampedModel._meta.abstract)

    def test_created_field_uses_auto_now_add(self):
        field = TimeStampedModel._meta.get_field("created")

        self.assertTrue(field.auto_now_add)

    def test_modified_field_uses_auto_now(self):
        field = TimeStampedModel._meta.get_field("modified")

        self.assertTrue(field.auto_now)


class AdminThemeTests(SimpleTestCase):
    def test_admin_login_uses_unfold_template(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "unfold")

    def test_builtin_admin_models_use_unfold(self):
        for model in (User, Group, TokenProxy):
            with self.subTest(model=model):
                self.assertIsInstance(admin.site._registry[model], ModelAdmin)
