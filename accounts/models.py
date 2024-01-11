import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email field is required.")

        if not username:
            raise ValueError("Username field is required.")

        if not first_name:
            raise ValueError("Firstname field is required.")

        if not last_name:
            raise ValueError("Lastname field is required.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_active = True
        # Designates whether the user has administrative privileges.
        user.role = RoleChoices.ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class RoleChoices(models.TextChoices):
    """
    numeration class representing different user roles
    """

    STUDENT = "student", "Student"
    INSTRUCTOR = "instructor", "Instructor"
    ADMIN = "admin", "Admin"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the application.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile = models.ImageField(
        default="default.jpg",
        upload_to="User Profiles/",
        null=True,
        blank=True,
    )
    headline = models.CharField(
        max_length=80,
        help_text="Add a professional headline like, 'Instructor at Udemy' or 'Architect.'",
        null=True,
        blank=True,
    )
    about = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
        help_text="Custom user roles (default: Student)",
    )

    # social media links
    website_link = models.URLField(
        null=True, blank=True, help_text="Input your Website URL."
    )
    twitter_url = models.URLField(
        blank=True, null=True, help_text="Input your Twitter profile URL."
    )
    facebook_url = models.URLField(
        blank=True, null=True, help_text=" Input your Facebook profile URL."
    )
    linkedin_url = models.URLField(
        blank=True, null=True, help_text="Input your LinkedIn profile URL."
    )
    youtube_url = models.URLField(
        blank=True, null=True, help_text="Input your Youtube profile URL."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
    )

    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def switch_role(self):
        """Switches the user's role between 'Student' and 'Instructor'."""
        if self.role == RoleChoices.STUDENT:
            self.role = RoleChoices.INSTRUCTOR
            self.save()
            return "Instructor"
        elif self.role == RoleChoices.INSTRUCTOR:
            self.role = RoleChoices.STUDENT
            self.save()
            return "Student"
        else:
            return self.role

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
