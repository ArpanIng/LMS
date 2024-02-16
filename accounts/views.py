from typing import Any
from django.contrib import messages
from django.contrib.auth import get_user_model, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser


from courses.models import Enrollment

from .forms import (
    CustomAuthenticationForm,
    ProfileForm,
    ProfilePhotoForm,
    RegistrationForm,
)

User = get_user_model()


def handle_users_redirect(request):
    """
    Raises a Http404 exception with a message indicating an invalid URL.
      - If a custom handler404 function is defined in the URL configuration, it will be invoked to handle the 404 error
      otherwise django's default 404 error handling behavior will be applied.
    """
    raise Http404("Invalid URL")


class RegistrationView(generic.FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        messages.success(self.request, "Account created sucessfully!")
        return super(RegistrationView, self).form_valid(form)


class CustomLoginView(views.LoginView):
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True
    template_name = "accounts/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password.")
        return super().form_invalid(form)


class CustomLogoutView(views.LogoutView):
    pass


class PublicProfileView(generic.View):
    def get(self, request, *args, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        if first_name and last_name:
            try:
                user = CustomUser.objects.get(
                    first_name__iexact=first_name, last_name__iexact=last_name
                )
            except CustomUser.DoesNotExist:
                messages.error(request, "User profile not found.")
                handle_users_redirect(request)

        return render(request, "accounts/public_profile.html", {"user": user})


class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.request.user)
        context = {
            "user": self.request.user,
            "form": form,
        }
        return render(request, "accounts/profile.html", context)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(self.request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        return render(request, "accounts/profile.html", {"form": form})


class ProfilePhotoView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        form = ProfilePhotoForm(instance=self.request.user)
        context = {
            "user": self.request.user,
            "form": form,
        }
        return render(request, "accounts/profile_photo.html", context)

    def post(self, request, *args, **kwargs):
        form = ProfilePhotoForm(
            self.request.POST,
            self.request.FILES,
            instance=self.request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile photo updated successfully.")
            return redirect("accounts:profile_photo")
        return render(request, "accounts/profile_photo.html", {"form": form})


class InstructorProfileView(generic.DetailView):
    model = CustomUser
    context_object_name = "instructor"
    template_name = "accounts/instructor_profile.html"


class CustomPasswordChangeView(views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change_form.html"


class CustomPasswordChangeDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_change_done.html"


class CustomPasswordResetView(views.PasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    template_name = "accounts/password_reset_form.html"


class CustomPasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class CustomPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
