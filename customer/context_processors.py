# myapp/context_processors.py

from .models import Cart, CartItem

def cart_item_count(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        cart_item_count = CartItem.objects.filter(cart=cart).count()
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id, is_active=True)
        cart_item_count = CartItem.objects.filter(cart=cart).count()

    return {'cart_item_count': cart_item_count}
