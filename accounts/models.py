from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        STAFF = 'STAFF', 'Staff'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=7, choices=Role.choices, default=Role.STUDENT)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_active = models.BooleanField(default=True)  # Required for authentication

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No additional fields required for createsuperuser

    objects = UserManager()  # Use the custom manager

    def save(self, *args, **kwargs):
        # Sync role with Django permissions
        if self.role == User.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == User.Role.STAFF:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Returns the short name for the user (first_name).
        """
        return self.first_name

    def __str__(self):
        return self.email
