from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.utils import timezone


from courses.models import Course

from .models import Cart, CartItem, Wishlist, WishlistItem


# def session_view(request):
#     # cart_obj = Cart.objects.get_or_new(request)
#     cart_id = request.session.get("cart_id", None)
#     qs = Cart.objects.filter(id=cart_id)
#     if qs.exists():
#         cart_obj = qs.first()
#         if request.user.is_authenticated and cart_obj.user is None:
#             cart_obj.user = request.user
#             cart_obj.save()
#     else:
#         cart_obj = Cart.objects.new(user=request.user)
#         request.session["cart_id "] = cart_obj.id
#     return render(request, "test.html")


def session_view(request):
    cart_session_key = "cart_id"
    cart_id = request.session.get(cart_session_key, None)
    if cart_id:
        # Check if the cart exists
        cart_obj = Cart.objects.get(id=cart_id)
    else:
        # Create a new cart if it doesn't exist
        cart_obj = Cart.objects.create(date_added=timezone.now())
        request.session[cart_session_key] = cart_obj.id
    # If the user is logged in, associate the cart with the logged-in user
    if request.user.is_authenticated:
        if not cart_obj.user:
            # If there's no user associated with the anonymous cart, associate it with the logged-in user
            cart_obj.user = request.user
            cart_obj.save()
    return render(request, "test.html")


# class CartAddView(View):
#     def post(self, request, *args, **kwargs):
#         course_slug = self.kwargs["course_slug"]
#         # get course slug from requested url
#         course_obj = get_object_or_404(Course, slug=course_slug)

#         cart_session_key = "cart_id"  # Use a unique session key for the cart
#         cart_id = request.session.get(cart_session_key, None)
#         if cart_id:  # check if cart exists
#             cart_obj = Cart.objects.get(id=cart_id)
#         else:
#             cart_obj = Cart.objects.create(date_added=timezone.now())
#             request.session[cart_session_key] = cart_obj.id

#         cart_item, created = CartItem.objects.get_or_create(
#             cart=cart_obj, course=course_obj
#         )
#         if created:
#             return redirect("carts:cart")

#         # if request.user.is_authenticated:
#         #     try:
#         #         existing_cart = Cart.objects.get(user=request.user)
#         #         for item in cart_obj.cartitem_set.all():
#         #             item.cart = existing_cart
#         #             item.save()
#         #     except Cart.DoesNotExist:
#         #         cart_obj.user = request.user
#         #         cart_obj.save()

#         else:
#             return redirect(course_obj.get_absolute_url())


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        course_slug = self.kwargs["course_slug"]
        course_obj = get_object_or_404(Course, slug=course_slug)

        cart_session_key = "cart_id"
        cart_id = request.session.get(cart_session_key, None)
        if cart_id:
            # Check if the cart exists
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            # Create a new cart if it doesn't exist
            cart_obj = Cart.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None
            )
            request.session[cart_session_key] = cart_obj.id

        # Check if the course is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart_obj, course=course_obj
        )

        if created:
            # Course already in the cart, update any necessary fields
            return redirect("carts:cart")

        # # If the user is logged in, associate the cart with the logged-in user
        # if request.user.is_authenticated:
        #     if cart_obj.user is None:
        #         # If there's no user associated with the anonymous cart, associate it with the logged-in user
        #         cart_obj.user = request.user
        #         cart_obj.save()
        #     else:
        #         # If there's already a user associated with the cart, merge the anonymous cart with the user's cart
        #         anonymous_cart = (
        #             Cart.objects.filter(user=None).exclude(id=cart_obj.id).first()
        #         )
        #         if anonymous_cart:
        #             for item in anonymous_cart.cartitem_set.all():
        #                 item.cart = cart_obj
        #                 item.save()
        #             anonymous_cart.delete()

        return redirect(course_obj.get_absolute_url())


# class CartAddView(LoginRequiredMixin, View):
#     def get(self, request, course_slug):
#         course = get_object_or_404(Course, slug=course_slug)
#         return redirect(course.get_absolute_url())

#     def post(self, request, course_slug):
#         user = self.request.user
#         course = get_object_or_404(Course, slug=course_slug)

#         # Try to get the user's cart, and create it if it doesn't exist
#         cart, cart_created = Cart.objects.get_or_create(user=user)

#         # Check if the course is already in the user's cart
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
#         if created:
#             return redirect("carts:cart")
#         else:
#             return redirect(course.get_absolute_url())


class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        return redirect(course.get_absolute_url())

    def post(self, request, course_slug):
        user = self.request.user
        course = get_object_or_404(Course, slug=course_slug)
        cart = get_object_or_404(Cart, user=user)

        try:
            cart_item = CartItem.objects.get(cart=cart, course=course)
            cart_item.delete()
            messages.success(request, "Course removed from cart.")
        except CartItem.DoesNotExist:
            messages.error(request, "Course not found in cart.")

        return redirect("carts:cart")


def calculate_totals(cart_items):
    """
    Calculate the total price, total discount price, and total regular price of cart items.
    Returns:
        Tuple: A tuple containing three values - total price, total discount price, and total regular price.
    """
    total_price = 0
    total_regular_price = 0
    total_discount_price = 0

    for item in cart_items:
        course = item.course
        if course.discount_price is not None:  # course has discount
            total_price += course.discount_price
            total_discount_price += course.regular_price - course.discount_price
        else:
            total_price += course.regular_price

        total_regular_price += course.regular_price

    return total_price, total_discount_price, total_regular_price


class CartView(View):
    """Display the user's cart."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = self.request.user
            cart = get_object_or_404(Cart, user=user)
            cart_items = CartItem.objects.filter(cart=cart)

            # tuple unpacking / assigns each value to its corresponding variable
            total_price, total_discount_price, total_regular_price = calculate_totals(
                cart_items
            )

            if total_regular_price > 0:
                total_discount_percentage = round(
                    (total_discount_price / total_regular_price) * 100
                )
            else:
                total_discount_percentage = 0

            context = {
                "cart_items": cart_items,
                "cart_item_count": cart_items.count(),
                "total_price": total_price,
                "total_regular_price": total_regular_price,
                "total_discount_price": total_discount_price,
                "total_discount_percentage": total_discount_percentage,
            }
            return render(request, "carts/cart.html", context)
        else:
            return render(request, "carts/cart.html")


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


# class CartSession(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
#     )
#     courses = models.ManyToManyField(Course, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     objects = CartManager()

#     def __str__(self):
#         return str(self.id)
