from django.urls import path

from . import views

app_name = "carts"
urlpatterns = [
    path("", views.CartView.as_view(), name="cart"),
    path("session/", views.session_view, name="session"),
    path(
        "add-to-cart/<slug:course_slug>/",
        views.CartAddView.as_view(),
        name="add_to_cart",
    ),
    path(
        "remove-from-cart/<slug:course_slug>/",
        views.CartRemoveView.as_view(),
        name="remove_from_cart",
    ),
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
