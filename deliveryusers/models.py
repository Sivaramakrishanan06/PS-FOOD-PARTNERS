# deliveryuser/models.py
from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant

class DeliveryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # This is required

    def __str__(self):
        return self.user.username
