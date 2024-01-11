from .models import Category


def menu_links(request):
    return {
        "all_categories": Category().get_top_categories.order_by("id"),
    }
