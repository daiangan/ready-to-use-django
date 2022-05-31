from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    def handle(self, *args, **options):

        def create_user_token():
            for user in User.objects.all():
                token = Token.objects.get_or_create(user=user)
                print(user, token)

        def get_users_tokens():
            for user in User.objects.all():
                token = Token.objects.get(user=user)
                print(user, '-', token)

        create_user_token()
        # get_users_tokens()
