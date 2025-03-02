# forms.py
from django import forms

class CustomerInfoForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Address', 'size' : '40'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'size' : '40'})
    )
    paytype = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'paytype'})
    )


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    Email = forms.EmailField(required=True)

    # class Meta:
    #     model = User
    #     Fields = ['username', 'email', 'password1', 'password2']