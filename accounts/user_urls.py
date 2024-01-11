from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.handle_users_redirect),
    path(
        "<uuid:pk>/", views.InstructorProfileView.as_view(), name="instructor_profile"
    ),
    path("edit-profile/", views.ProfileView.as_view(), name="profile"),
    path("edit-photo/", views.ProfilePhotoView.as_view(), name="profile_photo"),
    path(
        "<str:first_name>-<str:last_name>/",
        views.PublicProfileView.as_view(),
        name="public_profile",
    ),
]
