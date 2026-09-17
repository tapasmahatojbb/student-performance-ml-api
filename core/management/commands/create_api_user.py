import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Create production API user and token"

    def handle(self, *args, **options):
        username = os.environ.get("API_USERNAME")
        password = os.environ.get("API_PASSWORD")

        if not username or not password:
            self.stdout.write(
                "API_USERNAME/API_PASSWORD not configured. Skipping API user creation."
            )
            return

        user, created = User.objects.get_or_create(username=username)

        if created:
            user.set_password(password)
            user.save()

        Token.objects.get_or_create(user=user)

        self.stdout.write(
            self.style.SUCCESS("Production API user/token ready.")
        )
