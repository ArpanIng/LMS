from .models import Cart, CartItem


def cart_count(request):
    # cart_count = 0
    cart_id = request.session.get("cart_id")
    # cart = Cart.objects.filter(cart_id=cart_id)
    cart = Cart.objects.get(user=request.user)
    cart_count = CartItem.objects.filter(cart=cart)
    return {"cart_count": cart_count.count()}
