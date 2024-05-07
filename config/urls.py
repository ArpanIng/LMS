from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from instructors.views import Teach

# Configuring Django to use a custom 404 error handler globally
handler404 = "courses.error_handlers.handler404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", RedirectView.as_view(url="/", permanent=True)),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("courses.urls", namespace="courses")),
    path("cart/", include("carts.urls", namespace="carts")),
    path("account/", include("accounts.urls", namespace="accounts")),
    path("instructor/", include("instructors.urls", namespace="instructors")),
    path("user/", include("accounts.user_urls", namespace="users")),
]

urlpatterns += [
    path("teaching/", Teach.as_view(), name="teaching"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
