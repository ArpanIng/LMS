from django_ckeditor_5.widgets import CKEditor5Widget

from django import forms

from courses.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            "title",
            "summary",
            "description",
            "regular_price",
            "discount_price",
            "status",
            "featured_image",
            "is_free",
            "certificate",
            "level",
            "category",
            "subcategory",
            "language",
        )

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        attrs = {"class": "form-control"}
        for field_name, field in self.fields.items():
            if field_name not in ["description", "is_free", "certificate"]:
                field.widget.attrs.update(attrs)
