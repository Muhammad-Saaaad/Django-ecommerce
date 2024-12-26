from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50 , unique=True)
    password = models.CharField(max_length=120)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =[]
    
    objects = UserManager()