from django.contrib import admin

from .models import Wishlist, WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "date_added"]


admin.site.register(WishlistItem)
