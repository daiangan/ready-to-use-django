from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Create an authentication token for every user that does not have one."

    def handle(self, *args, **options):
        user_model = get_user_model()

        for user in user_model.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            status = "created" if created else "existing"
            self.stdout.write(f"{user} - {token} ({status})")
