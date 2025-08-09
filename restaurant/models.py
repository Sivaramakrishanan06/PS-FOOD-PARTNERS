# restaurant/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_item_images/', blank=True, null=True)

    def __str__(self):
        return self.name




class RestaurantStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"
    






