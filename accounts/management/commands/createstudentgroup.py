from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creates the Student group"

    def handle(self, *args, **kwargs):
        student_group, created = Group.objects.get_or_create(name="Student")
        if created:
            self.stdout.write(self.style.SUCCESS("Student group created successfully"))
        else:
            self.stdout.write(self.style.WARNING("Student group already exists"))
