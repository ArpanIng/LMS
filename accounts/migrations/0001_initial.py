# Generated by Django 4.2.4 on 2023-10-03 08:54

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "profile",
                    models.ImageField(
                        blank=True,
                        default="default.jpg",
                        null=True,
                        upload_to="User Profiles/",
                    ),
                ),
                (
                    "headline",
                    models.CharField(
                        blank=True,
                        help_text="Add a professional headline like, 'Instructor at Udemy' or 'Architect.'",
                        max_length=80,
                        null=True,
                    ),
                ),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("student", "Student"),
                            ("instructor", "Instructor"),
                            ("admin", "Admin"),
                        ],
                        default="student",
                        help_text="Custom user roles (default: Student)",
                        max_length=10,
                    ),
                ),
                (
                    "website_link",
                    models.URLField(
                        blank=True, help_text="Input your Website URL.", null=True
                    ),
                ),
                (
                    "twitter_url",
                    models.URLField(
                        blank=True,
                        help_text="Input your Twitter profile URL.",
                        null=True,
                    ),
                ),
                (
                    "facebook_url",
                    models.URLField(
                        blank=True,
                        help_text=" Input your Facebook profile URL.",
                        null=True,
                    ),
                ),
                (
                    "linkedin_url",
                    models.URLField(
                        blank=True,
                        help_text="Input your LinkedIn profile URL.",
                        null=True,
                    ),
                ),
                (
                    "youtube_url",
                    models.URLField(
                        blank=True,
                        help_text="Input your Youtube profile URL.",
                        null=True,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                    ),
                ),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
    ]
