from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserABC(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    role = models.CharField(max_length=5, choices=Roles.choices, default=Roles.USER)

    class Meta:
        abstract = True
