# deliveryuser/urls.py
from django.urls import path
from .views import DeliveryUserLoginView,custom_logout_delivery,delivery_user_dashboard,mark_order_as_delivered,delivery_order_detail



urlpatterns = [
    path('login/', DeliveryUserLoginView.as_view(), name='delivery_user_login'),
    path('dashboard/', delivery_user_dashboard, name='delivery_user_dashboard'),
    path('order/<int:order_id>/deliver/', mark_order_as_delivered, name='mark_order_as_delivered'),
    path('order/<int:order_id>/detail/', delivery_order_detail, name='delivery_order_detail'),
    path('logout/', custom_logout_delivery, name='custom_logout_delivery'),  # Custom logout URL
]
