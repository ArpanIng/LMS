from django.http import HttpResponseForbidden

from .models import RoleChoices


class StudentRequiredMixin:
    """Mixin to restrict views to students only."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != RoleChoices.STUDENT:
            return HttpResponseForbidden("403 Forbidden")
        return super().dispatch(request, *args, **kwargs)


class InstructorRequiredMixin:
    """Mixin to restrict views to instructors only."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != RoleChoices.INSTRUCTOR:
            return HttpResponseForbidden("403 Forbidden")
        return super().dispatch(request, *args, **kwargs)
