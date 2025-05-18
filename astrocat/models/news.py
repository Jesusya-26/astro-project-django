"""News db model is defined here."""

from django.db import models
from django.utils import timezone

from astrocat.models.users import User


class News(models.Model):
    """News entry authored by a user."""

    title = models.CharField(max_length=255, blank=True, null=False)
    content = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ["-id"]

    def __str__(self):
        return "<User post> " + self.title
