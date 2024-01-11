from django.urls import path

from carts.views import WishlistView
from instructors.views import CourseCreateView, CourseEditView, CourseDeleteView

from . import views

app_name = "courses"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("test/", views.test),
    path("contact/", views.ContactUsView.as_view(), name="contact"),
    path("about/", views.AboutView.as_view(), name="about"),
]

urlpatterns += [
    path("courses/search/", views.SearchView.as_view(), name="search"),
    path(
        "courses/<slug:category_slug>/",
        views.CourseByCategoryView.as_view(),
        name="courses_by_category",
    ),
    path(
        "courses/<slug:category_slug>/<slug:subcategory_slug>/",
        views.CourseBySubcategoryView.as_view(),
        name="courses_by_subcategory",
    ),
]

urlpatterns += [
    path(
        "my-courses/learning/",
        views.MyLearningView.as_view(),
        name="my_learning",
    ),
    path("my-courses/wishlist/", WishlistView.as_view(), name="wishlist"),
]


urlpatterns += [
    path("course/create/", CourseCreateView.as_view(), name="course_create"),
    path(
        "course/<slug:course_slug>/",
        views.CourseDetailView.as_view(),
        name="course_detail",
    ),
    path(
        "course/<slug:course_slug>/edit/",
        CourseEditView.as_view(),
        name="course_edit",
    ),
    path(
        "course/<slug:course_slug>/delete/",
        CourseDeleteView.as_view(),
        name="course_delete",
    ),
    path(
        "course/<slug:course_slug>/enroll/",
        views.CourseEnrollView.as_view(),
        name="course_enroll",
    ),
    path(
        "course/<slug:course_slug>/unenroll/",
        views.CourseUnenrollView.as_view(),
        name="course_unenroll",
    ),
    path(
        "course/<slug:course_slug>/learn/",
        views.CourseLessionView.as_view(),
        name="course_lesson",
    ),
]
