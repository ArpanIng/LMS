from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from carts.models import Cart, CartItem, Wishlist, WishlistItem

from .models import Category, Course, CourseLevel, Enrollment

User = get_user_model()


class IndexView(TemplateView):
    template_name = "courses/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fetches all published courses (6 records) with their associated instructors
        published_courses = Course.published.select_related("instructor").all()[:6]
        context["courses"] = published_courses
        return context


class CourseByCategoryOrSubcategoryView(ListView):
    """
    Displays a list of courses filtered by either category or subcategory.
    """

    model = Category
    context_object_name = "courses"
    template_name = "courses/courses_by_category_or_subcategory.html"

    def get_queryset(self):
        """
        Retrieves the queryset of courses based on the URL parameters.
        """

        if "category_slug" and "subcategory_slug" in self.kwargs:
            self.subcategory = get_object_or_404(
                self.model,
                slug=self.kwargs["subcategory_slug"],
            )
            courses = Course.objects.filter(
                subcategory=self.subcategory,
                status=Course.Status.PUBLISHED,
            ).select_related("instructor")
        else:
            self.category = get_object_or_404(
                self.model,
                slug=self.kwargs["category_slug"],
            )
            courses = Course.objects.filter(
                category=self.category,
                status=Course.Status.PUBLISHED,
            ).select_related("instructor", "level")
        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # retrives categories without any parent (top-level category)
        parent_categories = Category.objects.filter(
            slug=self.kwargs["category_slug"], parent__isnull=True
        )
        if "category_slug" and "subcategory_slug" in self.kwargs:
            context["title"] = self.subcategory
            context["course_count_by_subcategory"] = self.get_queryset().count()
        else:
            context["title"] = self.category
            context["course_count_by_category"] = self.get_queryset().count()
            context["request_page"] = "category"

        context["parent_categories"] = parent_categories
        context["course_levels"] = CourseLevel.objects.prefetch_related(
            "course_set"
        ).all()
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get("q") == "":
            return redirect("/")
        query = request.GET.get("q", None)
        if query:
            lookups = Q(title__icontains=query) | Q(description__icontains=query)
            search_results = Course.objects.filter(lookups).distinct()

        context = {
            "query": query,
            "search_results": search_results,
            "results_count": search_results.count(),
        }
        return render(request, "courses/search.html", context)


class CourseDetailView(DetailView):
    model = Course
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "course_slug"
    template_name = "courses/course_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.status == Course.Status.DRAFT:
            raise Http404("This course is not available.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        user = self.request.user

        if user.is_authenticated:
            # check if the student is already enrolled in the course
            is_enrolled = Enrollment.objects.filter(
                student=user, course=course
            ).exists()

            # check if the course is in in the user's wishlist
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            wishlist_item = WishlistItem.objects.filter(
                wishlist=wishlist, course=course
            ).exists()

            # check if the course is in the user's cart
            cart, created = Cart.objects.get_or_create(user=user)
            cartitem = CartItem.objects.filter(cart=cart, course=course).exists()

        else:
            is_enrolled = False
            wishlist_item = False
            cartitem = False

        context["enrolled"] = is_enrolled
        context["in_wishlist"] = wishlist_item
        context["in_cart"] = cartitem
        return context


class CourseEnrollView(LoginRequiredMixin, View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        return redirect(course.get_absolute_url())

    def post(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        user = self.request.user

        if Enrollment.objects.filter(student=user, course=course).exists():
            messages.info(
                request, message=f'You are already enrolled in course "{course.title}".'
            )
        else:
            try:
                Enrollment.objects.create(student=user, course=course)
                messages.success(
                    request,
                    f'You have successfully enrolled in course "{course.title}".',
                )
            except Exception as e:
                messages.error(
                    request,
                    f'An error occurred while enrolling in course "{course.title}": {e}',
                )
        return redirect("courses:my_learning")


class CourseUnenrollView(LoginRequiredMixin, View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        return redirect(course.get_absolute_url())

    def post(self, request, course_slug):
        user = self.request.user
        course = get_object_or_404(Course, slug=course_slug)
        enrollment = get_object_or_404(Enrollment, student=user, course=course)
        enrollment.delete()
        messages.success(
            request, f"You have successfully unenrolled from course “{course.title}”."
        )
        return redirect("courses:course_detail", course.slug)


class CourseLessionView(ListView):
    model = Course
    template_name = "courses/course_lesson.html"


class MyLearningView(LoginRequiredMixin, ListView):
    model = Enrollment
    context_object_name = "enrollments"
    template_name = "courses/my_learning.html"

    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "learning"
        return context


class StudentWishlistView(LoginRequiredMixin, ListView):
    model = Enrollment
    context_object_name = "enrollments"
    template_name = "carts/wishlist.html"

    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "wishlist"
        return context


def test(request):
    return render(request, "test_index.html")


class ContactUsView(TemplateView):
    template_name = "contact.html"


class AboutView(TemplateView):
    template_name = "about.html"
