from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creates the Instructor group"

    def handle(self, *args, **kwargs):
        instructor_group, created = Group.objects.get_or_create(name="Instructor")
        if created:
            self.stdout.write(
                self.style.SUCCESS("Instructor group created successfully")
            )
        else:
            self.stdout.write(self.style.WARNING("Instructor group already exists"))
