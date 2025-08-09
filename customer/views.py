import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView 

from customer.models import CartItem, Cart, MenuItem,Order,OrderItem
from customer.forms import UserForm, UserProfileForm
from customer.models import UserProfile
from restaurant.models import  Restaurant
from django.utils import timezone
from datetime import timedelta
from django.db.models import Min, Max

class LoginView(DjangoLoginView):
    template_name = 'customer/login.html'

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('menu')  # Redirect to the menu page or another page after registration
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'customer/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile_view(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect('profile_edit')  # Redirect if user profile does not exist

    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'customer/profile.html', context)

@login_required
def profile_edit(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect('profile_view')  # Redirect if user profile does not exist

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_view')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'customer/profile_edit.html', context)

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()
        restaurants = Restaurant.objects.all()
        context = {
            'menu_items': menu_items,
            'restaurants': restaurants #new added
        }
        return render(request, 'customer/menu.html', context)

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'customer/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })




class MenuItemDetail(View):
    def get(self, request, pk, *args, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=pk)
        # Get other items from the same restaurant, grouped by category
        restaurant_items = {}
        for item in MenuItem.objects.filter(restaurant=menu_item.restaurant).exclude(pk=pk):
            category = item.category  # Assuming MenuItem has a category field
            if category not in restaurant_items:
                restaurant_items[category] = []
            restaurant_items[category].append(item)

        context = {
            'menu_item': menu_item,
            'restaurant_items': restaurant_items,
        }
        return render(request, 'customer/menu_item_detail.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q", "")
        
        # Search in MenuItem model
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        # Search in Restaurant model
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )

        context = {
            'menu_items': menu_items,
            'restaurants': restaurants,
            'query': query
        }
        return render(request, 'customer/menu.html', context)
class AddToCartView(View):
    def post(self, request, pk):
        # Get the MenuItem object or return a 404 error if not found
        menu_item = get_object_or_404(MenuItem, pk=pk)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # For authenticated users, get or create a cart associated with the user
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            # For unauthenticated users, use session-based carts
            session_id = request.session.session_key
            if not session_id:
                request.session.create()  # Create a new session if none exists
                session_id = request.session.session_key

            # Get or create a cart associated with the session
            cart, created = Cart.objects.get_or_create(session_id=session_id, is_active=True)

        # Check if the cart contains items from a different restaurant
        cart_items = CartItem.objects.filter(cart=cart)
        if cart_items.exists() and cart_items.first().menu_item.restaurant != menu_item.restaurant:
            # Display a message to the user and ask if they want to clear the cart
            # Store the selected menu_item's id in the session to handle after confirmation
            request.session['new_menu_item_id'] = menu_item.id
            return redirect('cart_confirmation')  # Redirect to a confirmation page

        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
        if not created:
            # Increment quantity if the cart item already exists
            cart_item.quantity += 1
            cart_item.save()

        # Redirect to the menu page or any other page as needed
        referer_url = request.META.get('HTTP_REFERER', 'menu/')
        return redirect(referer_url)




class CartConfirmationView(View):
    def get(self, request):
        menu_item_id = request.session.get('new_menu_item_id')
        if not menu_item_id:
            return redirect('menu')

        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        return render(request, 'customer/cart_confirmation.html', {'menu_item': menu_item})

    def post(self, request):
        # Retrieve the cart based on the user's authentication status
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(session_id=request.session.session_key, is_active=True)
        
        # Clear the cart by deleting all related CartItem instances
        cart.items.all().delete()

        # Add the new item to the cart
        menu_item_id = request.session.pop('new_menu_item_id', None)
        if menu_item_id:
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            CartItem.objects.create(cart=cart, menu_item=menu_item, quantity=1)

        return redirect('menu')
























class ViewCartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()  # Create a new session if none exists
                session_id = request.session.session_key

            cart, created = Cart.objects.get_or_create(session_id=session_id, is_active=True)

        items = cart.items.all()
        total_amount = sum(item.menu_item.price * item.quantity for item in items)

        return render(request, 'customer/view_cart.html', {'cart_items': items, 'total_amount': total_amount})

class RemoveFromCartView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return redirect('view_cart')

class UpdateCartItemView(View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk)
        data = json.loads(request.body)
        quantity = data.get('quantity')

        if quantity and quantity.isdigit() and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid quantity'})







# @login_required
# def checkout(request):
#     user = request.user
#     cart = get_object_or_404(Cart, user=user, is_active=True)
    
#     if request.method == 'POST':
#         # Ensure there's only one restaurant in the cart
#         items = cart.items.all()
#         if not items:
#             return render(request, 'customer/checkout.html', {'cart': cart, 'error': 'No items in the cart'})
        
#         restaurant = items[0].menu_item.restaurant
        
#         # Calculate total amount for this restaurant
#         total_amount = sum(item.menu_item.price * item.quantity for item in items)
        
#         # Create a new cart for the items
#         new_cart = Cart.objects.create(user=user, is_active=False)
#         new_cart.items.set(items)
#         new_cart.save()
        
#         # Create an order for this new cart with the total amount and user
#         Order.objects.create(
#             cart=new_cart,
#             status='Pending',
#             total_amount=total_amount,
#             user=user
#         )
        
#         cart.is_active = False
#         cart.save()
#         return redirect('payment')
    
#     # Calculate item totals for the template
#     item_total = {item.id: item.menu_item.price * item.quantity for item in cart.items.all()}
#     total_amount = sum(item_total.values())

#     context = {
#         'cart': cart,
#         'restaurant': cart.items.first().menu_item.restaurant,
#         'item_total': item_total,
#         'total_amount': total_amount
#     }
#     return render(request, 'customer/checkout.html', context)




@login_required
def checkout(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user, is_active=True)
    
    if request.method == 'POST':
        items = cart.items.all()
        if not items:
            return render(request, 'customer/checkout.html', {'cart': cart, 'error': 'No items in the cart'})
        
        restaurant = items[0].menu_item.restaurant
        
        # Create a new cart for the items
        new_cart = Cart.objects.create(user=user, is_active=False)
        new_cart.items.set(items)
        new_cart.save()
        
        # Create an order for this new cart with the total amount and user
        order = Order.objects.create(
            cart=new_cart,
            status='Pending',
            total_amount=sum(item.menu_item.price * item.quantity for item in items),
            user=user
        )
        
        # Create OrderItem instances for each item in the cart
        for item in items:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity
            )
        
        cart.is_active = False
        cart.save()
        return redirect('payment')
    
    item_total = {item.id: item.menu_item.price * item.quantity for item in cart.items.all()}
    total_amount = sum(item_total.values())

    context = {
        'cart': cart,
        'restaurant': cart.items.first().menu_item.restaurant,
        'item_total': item_total,
        'total_amount': total_amount
    }
    return render(request, 'customer/checkout.html', context)


@login_required
def payment(request):
    if request.method == 'POST':
        # Retrieve all pending orders for the user
        orders = Order.objects.filter(user=request.user, status='Pending')

        if orders.exists():
            # Update the status to 'Paid' for all pending orders
            orders.update(status='Paid')

            # Redirect to the order confirmation page
            return redirect('order_confirmation')
        else:
            # Render the payment page with an error message if no pending orders are found
            return render(request, 'customer/payment.html', {
                'error': 'No pending orders found.'
            })

    # For GET requests, compute the total amount
    orders = Order.objects.filter(user=request.user, status='Pending')
    total_amount = sum(order.get_total_price() for order in orders)

    return render(request, 'customer/payment.html', {
        'total_amount': total_amount
    })







































@login_required
def order_confirmation(request):
    try:
        # Get the most recent order for the user
        order = Order.objects.filter(user=request.user).latest('created_at')

        # Initialize variables
        grand_total = 0
        item_details = []

        # Get all order items
        order_items = CartItem.objects.filter(cart=order.cart)  # Use correct related name

        for item in order_items:
            item_total = item.menu_item.price * item.quantity
            grand_total += item_total

            item_details.append({
                'name': item.menu_item.name,
                'quantity': item.quantity,
                'total': item_total
            })

        context = {
            'order': order,
            'grand_total': grand_total,
            'item_details': item_details
        }

    except Order.DoesNotExist:
        context = {
            'error': 'No orders found for this user.'
        }

    return render(request, 'customer/order_confirmation.html', context)



# @login_required
# def order_history(request):
#     user = request.user
#     orders = Order.objects.filter(user=user).order_by('-created_at')
    
#     context = {
#         'orders': orders,
#     }
    
#     return render(request, 'customer/order_history.html', context)

@login_required
def order_history(request):
    user = request.user
    filter_option = request.GET.get('filter', 'all')
    orders = Order.objects.filter(user=user).order_by('-created_at')

    # Apply filtering based on the selected filter option
    if filter_option == 'last6months':
        six_months_ago = timezone.now() - timedelta(days=180)
        orders = orders.filter(created_at__gte=six_months_ago)
    elif filter_option.isdigit():
        orders = orders.filter(created_at__year=int(filter_option))

    # Get the range of years for filtering options
    year_range = orders.aggregate(min_year=Min('created_at'), max_year=Max('created_at'))
    min_year = year_range['min_year'].year if year_range['min_year'] else timezone.now().year
    max_year = year_range['max_year'].year if year_range['max_year'] else timezone.now().year
    years = list(range(max_year, min_year - 1, -1))

    context = {
        'orders': orders,
        'filter': filter_option,
        'years': years,  # Pass the available years to the template
    }

    return render(request, 'customer/order_history.html', context)



@login_required
def customer_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    # Assuming all items in an order come from the same restaurant, fetch the restaurant name from the first item
    restaurant_name = items.first().menu_item.restaurant.name if items.exists() else None

    context = {
        'order': order,
        'items': items,
        'restaurant_name': restaurant_name,  # Pass the restaurant name to the template
    }
    return render(request, 'customer/order_detail.html', context)
