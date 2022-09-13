from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.signals import user_logged_in, user_logged_out
# from django.dispatch import receiver

class CustomUser(AbstractUser):
    # pass
    # add additional fields in here
    login_status = models.BooleanField(default=False)
    logout_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username



# @receiver(user_logged_in)
# def on_login(sender, user, request, **kwargs):
#     print('User just logged in....')
    
# @receiver(user_logged_out)
# def on_logout(sender, user, request, **kwargs):
#     print('User Just logged Out....')
	


        