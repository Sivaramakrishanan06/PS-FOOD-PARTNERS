# from django.contrib import admin

# # Register your models here.

# from .models import Category, Restaurant, MenuItem

# # Define how each model should appear in the admin interface

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# class RestaurantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address')
#     search_fields = ('name', 'address')

# class MenuItemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'restaurant', 'category', 'price')
#     list_filter = ('restaurant', 'category')
#     search_fields = ('name', 'description')

# # Register the models with the admin site

# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Restaurant, RestaurantAdmin)
# admin.site.register(MenuItem, MenuItemAdmin)

from django.contrib import admin
from .models import Restaurant, Category, MenuItem,  RestaurantStaff


admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(RestaurantStaff)


