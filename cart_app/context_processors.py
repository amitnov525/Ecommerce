from cart_app.models import Cart, CartItem 
from cart_app.views import _cart

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    try:
        cart_id=Cart.objects.get(cartid=_cart(request))
        cart_items=CartItem.objects.filter(cart=cart_id)
        for cart_item in cart_items:
            cart_count+=cart_item.quantity
            
    except Cart.DoesNotExist:
        cart_count=0
    return {'cart_count':cart_count}

