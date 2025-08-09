# customer/models.py

from django.db import models
from django.contrib.auth.models import User
from restaurant.models import MenuItem
from deliveryusers.models import DeliveryUser

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart {self.id} for user {self.user if self.user else 'guest'}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New field to assign orders to a delivery user
    assigned_to = models.ForeignKey(DeliveryUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
    def get_total_price(self):
        return sum(item.menu_item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"