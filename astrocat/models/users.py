"""Feedback db model is defined here."""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the same as username."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and return a new user."""
        if not email:
            raise ValueError("Email is required!")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a super-user"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for authentication and ownership tracking."""

    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    surname = models.CharField(max_length=150, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return "<User> " + self.username
