from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

        widgets = {
        'username':forms.TextInput(attrs={"class":'form-control'}),
        'password':forms.PasswordInput(attrs={"class":'form-control'}),
        }
        fields = '__all__'
       

        

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")