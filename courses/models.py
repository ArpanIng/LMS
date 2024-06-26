from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    """
    Model representing a category and its subcategories.
    Note:
        - To create a top-level category, do not specify the parent.
        - To create a subcategory, provide the parent category to which it belongs.
    """

    title = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    slug = models.SlugField(max_length=50, unique=True)
    icon = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def get_category_url(self):
        """return the URL of the category itself."""
        return reverse(
            "courses:courses_by_category",
            kwargs={"category_slug": self.slug},
        )

    def get_subcategory_url(self):
        """return the URL of the category and subcategory."""
        return reverse(
            "courses:courses_by_subcategory",
            kwargs={
                "category_slug": self.parent.slug,
                "subcategory_slug": self.slug,
            },
        )

    @staticmethod
    def get_top_categories():
        """Retrieve top-level categories with their subcategories prefetched."""
        return Category.objects.filter(parent__isnull=True).prefetch_related("children")


class CourseLevel(models.Model):
    """Model representing a level for a course."""

    title = models.CharField(
        max_length=50,
        help_text="Enter course level (e.g. Beginner, Intermediate, Advanced)",
        unique=True,
    )

    def __str__(self):
        return self.title


class Language(models.Model):
    """Model representing a language for a course."""

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="The full name of the language, e.g., 'English'.",
    )

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    """
    Custom Manager
    Returns: Course with 'PUBLISHED' status
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=Course.Status.PUBLISHED)


class Course(models.Model):
    """Model representing a course."""

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250, help_text="Enter course title.")
    slug = models.SlugField(max_length=250, unique=True)
    summary = models.CharField(max_length=800, help_text="Enter a summary of a course.")
    description = CKEditor5Field("Description", config_name="extends")
    regular_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price of the course.",
    )
    discount_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Discount price of the course.",
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Select the status of the course.",
    )
    featured_image = models.ImageField(
        default="default_course_image.jpg", upload_to="Courses/", null=True
    )
    is_free = models.BooleanField(
        default=False,
        help_text="Indicates whether the course is available for free or not.",
    )
    certificate = models.BooleanField(
        default=False,
        help_text="Indicates whether the course provides a certificate upon completion.",
    )
    level = models.ForeignKey(CourseLevel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        help_text="Assign parent category",
        related_name="parent_courses",
    )
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        help_text="Assign sub category",
        related_name="subcategory_courses",
        null=True,
        blank=True,
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
    )
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()  # default Manager
    published = PublishedManager()  # custom published Manager

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"course_slug": self.slug})

    def get_enroll_url(self):
        return reverse("courses:course_enroll", kwargs={"course_slug": self.slug})

    def get_unenroll_url(self):
        return reverse("courses:course_unenroll", kwargs={"course_slug": self.slug})

    def has_discount(self):
        """helps determine whether a course has a discount or not"""
        return self.discount_price is not None

    @property
    def get_discount_percentage(self):
        if self.has_discount():
            discount_percentage = round(
                ((self.regular_price - self.discount_price) / self.regular_price) * 100
            )
            return discount_percentage
        return 0  # Return 0 when the regular_price is 0 to avoid division by zero error

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_free:
            self.regular_price = None  # will be saved as null in database
            self.discount_price = None
        return super(Course, self).save(*args, **kwargs)


class CourseRequirement(models.Model):
    """Model representing a requirement for a course."""

    content = models.CharField(
        max_length=500,
        help_text="Enter any prerequisites or requirements for students before enrolling in the course.",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="requirements",
        help_text="The course to which this requirement belongs.",
    )

    def __str__(self):
        return self.content


class WhatYoullLearn(models.Model):
    """
    Model representing topics or skills covered in a course/ What you'll learn section.
    """

    content = models.CharField(
        max_length=255,
        help_text="Enter the specific topic or skill covered in the course.",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="topics",
        help_text="Select the course to which this topic belongs.",
    )

    def __str__(self):
        return self.content


class Module(models.Model):
    """Model representing a module within a course."""

    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Specify the order in which this module should appear in the course.",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        help_text="Select the corresponding course to associate this module with.",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Model representing a lesson within a module."""

    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(
        help_text="Specify the order in which this lesson should appear in the course."
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


# class Video(models.Model):
#     """
#     Model representing a video related to a specific lesson.
#     """

#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
#     title = models.CharField(max_length=255)
#     video_url = models.URLField(
#         validators=[URLValidator()],
#         help_text="Enter the URL of the video hosted on a video platform.",
#     )
#     thumbnail = models.ImageField(upload_to="Video Thumbnails/", null=True)
#     description = models.TextField(blank=True, null=True)
#     duration = models.FloatField(null=True)
#     is_preview = models.BooleanField(default=False)
#     created = models.DateTimeField(default=timezone.now)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title


class Enrollment(models.Model):
    """Model representing the enrollment of a student in a course."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrollment_date = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student}: {self.course.title}"
