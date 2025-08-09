from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem, RestaurantStaff,Category
from customer.models import Order,Cart
from .forms import RestaurantForm, MenuItemForm, RestaurantStaffForm,CategoryForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib import messages
from datetime import date, datetime
from deliveryusers.forms import  DeliveryUserForm




class RestaurantLoginView(DjangoLoginView):
    template_name = 'restaurant/login.html'
    success_url = reverse_lazy('restaurant_profile')

def custom_logout(request):
    logout(request)
    return redirect('index')

def restaurant_profile(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    return render(request, 'restaurant/restaurant_profile.html', {'restaurant': restaurant})


@login_required
def add_category(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant

    if request.method == 'POST':
        form = CategoryForm(request.POST, restaurant=restaurant)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = CategoryForm(restaurant=restaurant)

    return render(request, 'restaurant/add_category.html', {'form': form})



@login_required
@require_POST
def edit_category(request, pk):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)

    category.name = request.POST.get('category_name')
    category.save()
    return redirect('manage_menu')






@login_required
@require_POST
def delete_category(request, pk):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    category = get_object_or_404(Category, pk=pk, restaurant=restaurant)
    category.delete()
    return redirect('manage_menu')




def manage_menu(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    # categories = Category.objects.all()
    categories = Category.objects.filter(restaurant=restaurant)
    paginator = Paginator(menu_items, 10)  # Show 10 menu items per page
    page_number = request.GET.get('page')
    menu_items = paginator.get_page(page_number)
    return render(request, 'restaurant/manage_menu.html', {
        'menu_items': menu_items,
        'categories': categories,
        'restaurant': restaurant
    })


@login_required
def add_menu_item(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, staff=staff)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = staff.restaurant
            menu_item.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(staff=staff)
    
    return render(request, 'restaurant/add_menu_item.html', {'form': form})

@login_required
def edit_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    if menu_item.restaurant != staff.restaurant:
        return redirect('manage_menu')
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item, staff=staff)
        if form.is_valid():
            form.save()
            return redirect('manage_menu')
    else:
        form = MenuItemForm(instance=menu_item, staff=staff)
    return render(request, 'restaurant/edit_menu_item.html', {'form': form})

@login_required
def delete_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    if menu_item.restaurant == staff.restaurant:
        menu_item.delete()
    return redirect('manage_menu')



# @login_required
# def order_management(request):
#     staff = get_object_or_404(RestaurantStaff, user=request.user)
#     restaurant = staff.restaurant

#     # Get orders where any cart item belongs to the staff's restaurant, ordered by creation date descending
#     orders = Order.objects.filter(cart__items__menu_item__restaurant=restaurant).distinct().order_by('-created_at')

#     return render(request, 'restaurant/order_management.html', {'orders': orders, 'restaurant': restaurant})


@login_required
def order_management(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant

    # Get the selected date from the request (if any)
    selected_date_str = request.GET.get('date')
    
    if selected_date_str:
        try:
            # Parse date from string using the format 'd M, Y'
            selected_date = datetime.strptime(selected_date_str, '%d %b, %Y').date()
        except ValueError:
            selected_date = date.today()  # Fallback if parsing fails
    else:
        selected_date = date.today()  # Default to today's date

    # Filter orders by the selected date
    orders = Order.objects.filter(
        cart__items__menu_item__restaurant=restaurant,
        created_at__date=selected_date
    ).distinct().order_by('-created_at')

    # Get a list of all distinct dates that have orders
    order_dates = Order.objects.filter(
        cart__items__menu_item__restaurant=restaurant
    ).dates('created_at', 'day', order='DESC').distinct()

    return render(request, 'restaurant/order_management.html', {
        'orders': orders,
        'restaurant': restaurant,
        'selected_date': selected_date,
        'order_dates': order_dates,
    })


# @login_required
# def order_management(request):
#     staff = get_object_or_404(RestaurantStaff, user=request.user)
#     restaurant = staff.restaurant

#     # Get the selected date from the request (if any)
#     selected_date_str = request.GET.get('date')
    
#     if selected_date_str:
#         # Parse date from string using strptime with the format matching your date string
#         selected_date = datetime.strptime(selected_date_str, '%b. %d, %Y').date()
#     else:
#         selected_date = date.today()  # Default to today's date

#     # Filter orders by the selected date
#     orders = Order.objects.filter(
#         cart__items__menu_item__restaurant=restaurant,
#         created_at__date=selected_date
#     ).distinct().order_by('-created_at')

#     # Get a list of all distinct dates that have orders
#     order_dates = Order.objects.filter(
#         cart__items__menu_item__restaurant=restaurant
#     ).dates('created_at', 'day', order='DESC').distinct()

#     return render(request, 'restaurant/order_management.html', {
#         'orders': orders,
#         'restaurant': restaurant,
#         'selected_date': selected_date,
#         'order_dates': order_dates,
#     })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.cart.items.all()

    # Prepare item totals
    for item in order_items:
        item.total_price = item.quantity * item.menu_item.price

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'restaurant/order_detail.html', context)

# @login_required
# def update_order_to_delivering(request, order_id):
#     staff = get_object_or_404(RestaurantStaff, user=request.user)
#     order = get_object_or_404(Order, id=order_id)

#     # Check if the order belongs to the staff's restaurant
#     if order.cart.items.filter(menu_item__restaurant=staff.restaurant).exists():
#         order.status = 'Delivering'
#         order.save()
#     else:
#         # Optional: Add feedback if the order does not belong to the staff's restaurant
#         messages.error(request, "You cannot update this order as it doesn't belong to your restaurant.")

#     return redirect('order_management')


# @login_required
# def update_order_to_delivering(request, order_id):
#     staff = get_object_or_404(RestaurantStaff, user=request.user)
#     order = get_object_or_404(Order, id=order_id)

#     # Check if the order belongs to the staff's restaurant
#     if order.cart.items.filter(menu_item__restaurant=staff.restaurant).exists():
#         # Find available delivery users for the restaurant
#         available_delivery_users = DeliveryUser.objects.filter(restaurant=staff.restaurant, user__is_active=True)

#         if available_delivery_users.exists():
#             # Assign the order to the first available delivery user (or you can implement your own logic)
#             order.assigned_to = available_delivery_users.first()
#             order.status = 'Delivering'
#             order.save()
#             messages.success(request, "Order updated to 'Delivering' and assigned to a delivery user.")
#         else:
#             messages.error(request, "No available delivery users for your restaurant.")
#     else:
#         messages.error(request, "You cannot update this order as it doesn't belong to your restaurant.")

#     return redirect('order_management')


@login_required
def update_order_to_delivering(request, order_id):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the staff's restaurant
    if order.cart.items.filter(menu_item__restaurant=staff.restaurant).exists():
        # Get delivery users for the restaurant and convert to list
        available_delivery_users = list(DeliveryUser.objects.filter(restaurant=staff.restaurant).order_by('user__username'))

        if available_delivery_users:
            # Find the last assigned delivery user
            last_order = Order.objects.filter(
                status='Delivering',
                cart__items__menu_item__restaurant=staff.restaurant
            ).order_by('-updated_at').first()

            if last_order and last_order.assigned_to:
                # Find index of the last assigned delivery user
                last_assigned_user = last_order.assigned_to
                try:
                    last_index = available_delivery_users.index(last_assigned_user)
                except ValueError:
                    # If the last assigned user is not in the list, start from the beginning
                    last_index = -1
                next_index = (last_index + 1) % len(available_delivery_users)
            else:
                # If no previous assignments, start with the first delivery user
                next_index = 0

            # Assign the next delivery user
            next_delivery_user = available_delivery_users[next_index]
            order.status = 'Delivering'
            order.assigned_to = next_delivery_user  # Ensure 'assigned_to' field exists in Order model
            order.save()

            messages.success(request, 'Order status updated to Delivering and assigned to {}.'.format(next_delivery_user.user.username))
        else:
            messages.error(request, "No delivery users available for this restaurant.")
    else:
        messages.error(request, "You cannot update this order as it doesn't belong to your restaurant.")

    return redirect('order_management')



@login_required
def update_order_to_cancelled(request, order_id):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the staff's restaurant
    if order.cart.items.filter(menu_item__restaurant=staff.restaurant).exists():
        order.status = 'Cancelled'
        order.save()
    else:
        # Optional: Add feedback if the order does not belong to the staff's restaurant
        messages.error(request, "You cannot cancel this order as it doesn't belong to your restaurant.")

    return redirect('order_management')






from deliveryusers.models import DeliveryUser


@login_required
def add_delivery_user(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant

    if request.method == 'POST':
        form = DeliveryUserForm(request.POST, request.FILES, user=None)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()

            delivery_user = form.save(commit=False)
            delivery_user.user = user
            delivery_user.restaurant = restaurant
            delivery_user.save()

            messages.success(request, 'Delivery user created successfully.')
            return redirect('view_delivery_users')
    else:
        form = DeliveryUserForm(user=None)

    return render(request, 'restaurant/add_delivery_user.html', {'form': form})

@login_required
def view_delivery_users(request):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    delivery_users = DeliveryUser.objects.filter(restaurant=restaurant)
    
    return render(request, 'restaurant/view_delivery_users.html', {'delivery_users': delivery_users})

@login_required
def edit_delivery_user(request, pk):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    delivery_user = get_object_or_404(DeliveryUser, pk=pk, restaurant=restaurant)
    user = delivery_user.user

    if request.method == 'POST':
        form = DeliveryUserForm(request.POST, instance=delivery_user, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery user updated successfully.')
            return redirect('view_delivery_users')
    else:
        form = DeliveryUserForm(instance=delivery_user, user=user)

    return render(request, 'restaurant/edit_delivery_user.html', {'form': form})

@login_required
def delete_delivery_user(request, pk):
    staff = get_object_or_404(RestaurantStaff, user=request.user)
    restaurant = staff.restaurant
    delivery_user = get_object_or_404(DeliveryUser, pk=pk, restaurant=restaurant)

    user = delivery_user.user
    delivery_user.delete()  # Delete the DeliveryUser instance
    user.delete()  # Delete the corresponding User instance

    messages.success(request, 'Delivery user deleted successfully.')
    return redirect('view_delivery_users')