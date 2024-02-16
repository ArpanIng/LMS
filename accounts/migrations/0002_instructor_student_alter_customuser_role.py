# Generated by Django 4.2.4 on 2024-02-16 13:39

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Instructor",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("accounts.customuser",),
            managers=[
                ("instructors", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("accounts.customuser",),
            managers=[
                ("students", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Admin"),
                    ("STUDENT", "Student"),
                    ("INSTRUCTOR", "Instructor"),
                ],
                max_length=10,
            ),
        ),
    ]
