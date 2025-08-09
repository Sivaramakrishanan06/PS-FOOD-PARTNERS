from django import forms
from .models import Restaurant, MenuItem, RestaurantStaff,Category
from django.contrib.auth.hashers import make_password

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'phone', 'email', 'description', 'image']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        staff = kwargs.pop('staff', None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        
        if staff:
            # Filter categories based on the staff's restaurant
            self.fields['category'].queryset = Category.objects.filter(restaurant=staff.restaurant)
            
            # Add the restaurant field and set it to hidden and not required
            self.fields['restaurant'] = forms.ModelChoiceField(
                queryset=Restaurant.objects.filter(pk=staff.restaurant.pk), 
                initial=staff.restaurant, 
                widget=forms.HiddenInput(),
                required=False
            )


class RestaurantStaffForm(forms.ModelForm):
    class Meta:
        model = RestaurantStaff
        fields = ['user', 'restaurant']
        widgets = {
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'restaurant': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super().save(commit=False)
        if self.restaurant:
            category.restaurant = self.restaurant
        if commit:
            category.save()
        return category
    




