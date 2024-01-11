from django.urls import path

from . import views


app_name = "instructors"

urlpatterns = [
    path("courses/", views.Courses.as_view(), name="courses"),
    path("my-courses/", views.CourseListview.as_view(), name="course_list"),
    path("communication/qa/", views.Communication.as_view(), name="communication"),
    path("tools/", views.Tools.as_view(), name="tools"),
    path("help/", views.Resources.as_view(), name="resources"),
]
