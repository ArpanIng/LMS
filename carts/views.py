from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from courses.models import Course

from .carts import Cart
from .models import CartItem, Wishlist, WishlistItem


class AddToCartView(View):
    pass


def add_to_cart(request):
    # get the cart
    cart = Cart(request)
    if request.POST.get("action") == "post":
        course_id = int(request.POST.get("course_id"))
        course = get_object_or_404(Course, id=course_id)
        # save the session
        cart.add(course=course)
        messages.success(request, "Course added successfully.")
        # get cart quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({"Success": "Course added to the cart."})
        return response


def remove_from_cart(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        course_id = int(request.POST.get("course_id"))
        cart.delete(course=course_id)
        messages.success(request, "Course removed successfully.")
        response = JsonResponse({"course": "Course removed from the cart."})
        return response


class CartView(View):
    pass


def cart_view(request):
    # get the cart
    cart = Cart(request)
    cart_courses = cart.get_courses()
    cart_total = cart.calculate_totals()
    # tuple unpacking / assigns each value to its corresponding variable
    total_price, total_discount_percentage, total_regular_price = (
        cart.calculate_totals()
    )

    context = {
        "cart_courses": cart_courses,
        "total_price": total_price,
        "total_discount_percentage": total_discount_percentage,
        "total_regular_price": total_regular_price,
    }
    return render(request, "carts/cart.html", context)


# class AddToCartView(View):
#     def post(self, request, course_id, *args, **kwargs):
#         course_obj = get_object_or_404(Course, id=course_id)  # Get course

#         cart_session_key = "cart_id"
#         cart_id = request.session.get(cart_session_key, None)

#         if cart_id:  # check if cart exists
#             cart_obj = Cart.objects.get(id=cart_id)
#         else:  # Create a new cart
#             cart_obj = Cart.objects.create()
#             request.session[cart_session_key] = cart_obj.id

#         # Check if the course already exists in the cart
#         cart_item = cart_obj.cartitem_set.filter(course=course_obj).first()
#         if cart_item:
#             # Course already exists in the cart, display a message
#             messages.warning(request, "This course is already in your cart.")
#             return redirect(course_obj.get_absolute_url())
#         else:
#             cartitem = CartItem.objects.create(cart=cart_obj, course=course_obj)
#             cartitem.save()
#             return redirect("carts:cart")


# class RemoveFromCartView(View):
#     def post(self, request, course_id, *args, **kwargs):
#         course_obj = get_object_or_404(Course, id=course_id)

#         cart_session_key = "cart_id"
#         cart_id = request.session.get(cart_session_key, None)

#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#         else:
#             pass

#         cart_item = cart_obj.cartitem_set.filter(course=course_obj).first()
#         if cart_item:
#             cart_item.delete()
#             messages.success(request, "Course removed from cart.")
#         else:
#             messages.error(request, "Course not found in cart.")

#         return redirect("carts:cart")


# class CartView(View):
#     """Display the user's cart."""

#     def get(self, request, *args, **kwargs):
#         cart_session_key = "cart_id"
#         cart_id = request.session.get(cart_session_key, None)

#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             cart_items = CartItem.objects.filter(cart=cart_obj).order_by("-date_added")

#             # tuple unpacking / assigns each value to its corresponding variable
#             total_price, total_discount_percentage, total_regular_price = (
#                 cart_obj.calculate_totals()
#             )

#             context = {
#                 "cart_items": cart_items,
#                 "cart_item_count": cart_items.count(),
#                 "total_price": total_price,
#                 "total_discount_percentage": total_discount_percentage,
#                 "total_regular_price": total_regular_price,
#             }
#             return render(request, "carts/cart.html", context)
#         else:
#             return render(request, "carts/empty_cart.html")


class WishlistAddView(LoginRequiredMixin, View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        return redirect(course.get_absolute_url())

    def post(self, request, course_slug):
        user = self.request.user
        course = get_object_or_404(Course, slug=course_slug)

        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, course=course
        )
        if created:
            return redirect("courses:wishlist")


class WishlistRemoveView(LoginRequiredMixin, View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        return redirect("courses:course_detail", course.slug)

    def post(self, request, course_slug):
        user = self.request.user
        course = get_object_or_404(Course, slug=course_slug)
        wishlist = get_object_or_404(Wishlist, user=user)
        try:
            wishlist_item = WishlistItem.objects.get(wishlist=wishlist, course=course)
            wishlist_item.delete()
            messages.success(request, "Course removed from wishlist.")
        except WishlistItem.DoesNotExist:
            pass
        return redirect("courses:wishlist")


class WishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        template_name = "carts/wishlist.html"

        try:
            wishlist = Wishlist.objects.get(user=user)
        except:
            return render(request, template_name)

        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
        return render(request, template_name, {"wishlist_items": wishlist_items})


def checkout_view(request):
    return render(request, "carts/checkout.html")
