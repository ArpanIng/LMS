from django.core.exceptions import PermissionDenied

from accounts.models import CustomUser, RoleChoices


def is_student(user):
    return user.role == RoleChoices.STUDENT


def is_instructor(user):
    return user.role == RoleChoices.INSTRUCTOR


def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not is_student(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def instructor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not is_instructor(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
