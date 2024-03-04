from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creates the Admin group"

    def handle(self, *args, **kwargs):
        admin_group, created = Group.objects.get_or_create(name="Admin")
        if created:
            self.stdout.write(self.style.SUCCESS("Admin group created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Admin group already exists"))
