from django.urls import path

from . import views

app_name = "carts"
urlpatterns = [
    # path("", views.CartView.as_view(), name="cart"),
    path("", views.cart_view, name="cart"),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("remove/", views.remove_from_cart, name="remove_from_cart"),
    # path(
    #     "add-to-cart/<int:course_id>/",
    #     views.AddToCartView.as_view(),
    #     name="add_to_cart",
    # ),
    # path(
    #     "remove-from-cart/<int:course_id>/",
    #     views.RemoveFromCartView.as_view(),
    #     name="remove_from_cart",
    # ),
    path(
        "add-to-wishlist/<slug:course_slug>/",
        views.WishlistAddView.as_view(),
        name="add_to_wishlist",
    ),
    path(
        "remove-from-wishlist/<slug:course_slug>/",
        views.WishlistRemoveView.as_view(),
        name="remove_from_wishlist",
    ),
    path("checkout/", views.checkout_view, name="checkout"),
]
