from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    profilePic=models.ImageField(upload_to='profileImage',blank=True,null=True)

     # Specify related names for the groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )