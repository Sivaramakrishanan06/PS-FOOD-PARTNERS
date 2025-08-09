from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import (
    Index, About, Menu, MenuItemDetail, MenuSearch, restaurant_detail,
    AddToCartView, ViewCartView, UpdateCartItemView, RemoveFromCartView,CartConfirmationView,
    register, LoginView, profile_view, profile_edit, checkout, payment,
    order_confirmation,order_history,customer_order_detail
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(next_page='menu'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    # User Profile
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    # Home and About
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),

    # Menu
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),



    path('restaurant/<int:pk>/', restaurant_detail, name='restaurant-detail'),

    # Cart
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart-confirmation/', CartConfirmationView.as_view(), name='cart_confirmation'),
    path('view-cart/', ViewCartView.as_view(), name='view_cart'),
    path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-cart-item/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),

    # Checkout, Payment, and Order Confirmation
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
    path('order-history/', order_history, name='order_history'),
    path('order/<int:order_id>/', customer_order_detail, name='customer_order_detail'),
    
    # Include other app urls
    path('restaurant/', include('restaurant.urls')),
    path('deliveryusers/', include('deliveryusers.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
