"""Feedback db model is defined here."""

from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    """Feedback message submitted by a user."""

    name = models.CharField("user name", max_length=100)
    email = models.EmailField("user e-mail")
    message = models.TextField("message content")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.email})"
