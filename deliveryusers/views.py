from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import DeliveryUser 
from customer.models import  Order
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from customer.models import UserProfile

class DeliveryUserLoginView(LoginView):
    template_name = 'deliveryusers/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirect to the delivery user's dashboard page
        return reverse_lazy('delivery_user_dashboard')
    

@login_required
def custom_logout_delivery(request):
    logout(request)
    return redirect('delivery_user_login') 




@login_required
def delivery_user_dashboard(request):
    delivery_user = get_object_or_404(DeliveryUser, user=request.user)
    
    # Fetch orders assigned to this delivery user
    orders = Order.objects.filter(assigned_to=delivery_user).order_by('-id')
    
    context = {
        'orders': orders,
    }
    return render(request, 'deliveryusers/dashboard.html', context)



# views.py
# views.py
@login_required
def delivery_order_detail(request, order_id):
    delivery_user = get_object_or_404(DeliveryUser, user=request.user)
    order = get_object_or_404(Order, id=order_id, assigned_to=delivery_user)
    
    # Access customer through the User model
    customer = order.user
    customer_profile = get_object_or_404(UserProfile, user=customer)
    
    context = {
        'order': order,
        'customer': customer,
        'customer_profile': customer_profile,
    }
    return render(request, 'deliveryusers/delivery_order_detail.html', context)



@login_required
def mark_order_as_delivered(request, order_id):
    delivery_user = get_object_or_404(DeliveryUser, user=request.user)
    order = get_object_or_404(Order, id=order_id, assigned_to=delivery_user)

    # Check if the order's current status is 'Delivering'
    if order.status == 'Delivering':
        order.status = 'Delivered'
        order.save()

        messages.success(request, 'Order marked as Delivered successfully.')
    else:
        messages.error(request, 'Order status is not Delivering and cannot be marked as Delivered.')

    return redirect('delivery_user_dashboard')  # Redirect to a relevant page for delivery users
