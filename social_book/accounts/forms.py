from django import forms
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name', 'address', 'birth_year', 'public_visibility')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'address', 'birth_year', 'public_visibility') # noqa
