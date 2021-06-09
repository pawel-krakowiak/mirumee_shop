from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self,email, password=None, is_active=True, **extra_fields):
        email = UserManager.normalize_email(email)

        extra_fields.pop('username',None)

        user = self.model(
            email=email,
            is_active=is_active,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()