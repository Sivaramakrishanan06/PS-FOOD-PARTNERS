from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('restaurant/login/', views.RestaurantLoginView.as_view(), name='restaurant_login'),
    path('restaurant/profile/', views.restaurant_profile, name='restaurant_profile'),
     path('logout/', views.custom_logout, name='logout'),
   
    path('add-category/', views.add_category, name='add_category'),
    path('edit_category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),

    path('manage_menu/', views.manage_menu, name='manage_menu'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('edit_menu_item/<int:pk>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:pk>/', views.delete_menu_item, name='delete_menu_item'),
     path('order-management/', views.order_management, name='order_management'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    path('order/<int:order_id>/deliver/', views.update_order_to_delivering, name='update_order_to_delivering'),
    path('order/<int:order_id>/cancel/', views.update_order_to_cancelled, name='update_order_to_cancelled'),

    path('delivery_users/add/', views.add_delivery_user, name='add_delivery_user'),
    path('delivery_users/', views.view_delivery_users, name='view_delivery_users'),
    path('delivery_users/edit/<int:pk>/', views.edit_delivery_user, name='edit_delivery_user'),
    path('delivery_users/delete/<int:pk>/', views.delete_delivery_user, name='delete_delivery_user'),
]
