from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from accounts.role_mixins import InstructorRequiredMixin
from courses.models import Category, Course

from .forms import CourseForm


class Teach(View):
    def get(self, request, *args, **kwargs):
        return render(request, "instructors/teaching.html")


class Courses(LoginRequiredMixin, InstructorRequiredMixin, TemplateView):
    template_name = "instructors/courses.html"


class Communication(LoginRequiredMixin, InstructorRequiredMixin, TemplateView):
    template_name = "instructors/communication.html"


class Tools(LoginRequiredMixin, InstructorRequiredMixin, TemplateView):
    template_name = "instructors/tools.html"


class Resources(LoginRequiredMixin, InstructorRequiredMixin, TemplateView):
    template_name = "instructors/resources.html"


class CourseCreateView(LoginRequiredMixin, InstructorRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "instructors/course_create.html"

    def get_form(self, form_class=None):
        """Override the form instantiation process to customize field choices."""
        form = super().get_form(form_class)
        form.fields["category"].queryset = Category.objects.filter(parent=None)
        form.fields["subcategory"].queryset = Category.objects.filter(
            parent__isnull=False
        )
        return form

    def form_valid(self, form):
        form.instance.instructor = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Course created successfully!")
        return response


class CourseListview(LoginRequiredMixin, InstructorRequiredMixin, ListView):
    model = Course
    context_object_name = "course_list"
    template_name = "instructors/course_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(instructor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_courses"] = self.get_queryset().count()
        return context


class CourseEditView(
    LoginRequiredMixin, InstructorRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Course
    form_class = CourseForm
    slug_field = "slug"
    slug_url_kwarg = "course_slug"
    template_name = "instructors/course_edit.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Course details updated successfully.")
        return response

    def test_func(self):
        course = self.get_object()
        return course.instructor == self.request.user


class CourseDeleteView(LoginRequiredMixin, InstructorRequiredMixin, DeleteView):
    model = Course
    template_name = "instructors/course_delete.html"
