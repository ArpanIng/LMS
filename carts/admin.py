from django.contrib import admin

from .models import Cart, CartItem, Wishlist, WishlistItem

admin.site.register(Cart)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ["date_added"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "date_added"]


admin.site.register(WishlistItem)
