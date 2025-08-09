from customer.models import Cart, Order

# List all active carts and their associated orders
for cart in Cart.objects.filter(is_active=True):
    orders_for_cart = Order.objects.filter(cart=cart)
    print(f"Cart ID: {cart.id}, Orders: {orders_for_cart}")
