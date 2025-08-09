# deliveryusers/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import DeliveryUser
from django.contrib.auth.forms import AuthenticationForm

class DeliveryUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    phone_number = forms.CharField(max_length=20, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = DeliveryUser
        fields = ['phone_number', 'address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            # Initialize User fields with existing values
            self.fields['username'].initial = self.user.username
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if self.cleaned_data['password1']:
                self.user.set_password(self.cleaned_data['password1'])
            if commit:
                self.user.save()

        delivery_user = super().save(commit=False)
        delivery_user.user = self.user
        if commit:
            delivery_user.save()
        return delivery_user






class DeliveryUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
