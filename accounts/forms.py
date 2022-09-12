from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
# from django.forms import TextInput, EmailField, PasswordInput

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

        widgets = {
        'username':forms.TextInput(attrs={"class":'form-control text-center', 'placeholder': 'Username: LETTERS, DIGITS AND @/./+/-/_ ONLY.'}),
        'email':forms.EmailInput(attrs={"class":'form-control text-center', 'placeholder': 'Email'}),
        # 'password1':forms.PasswordInput(attrs={"class":'form-control', 'placeholder': 'Password: AT LEAST 8 CHARACTERS'}),
        # 'password2':forms.PasswordInput(attrs={"class":'form-control', 'placeholder': 'Confirm Password'}),
        }
        # fields = '__all__'

        # def __init__(self, *args, **kwargs):
        #     super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        #     self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password','required': 'required'}
        #     self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
        #     self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
       

        

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

        widgets = {
        'username':forms.TextInput(attrs={"class":'form-control', 'placeholder': 'Username'}),
        'password':forms.PasswordInput(attrs={"class":'form-control', 'placeholder': 'Password'}),
        }
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password','required': 'required'}
            self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
            
       