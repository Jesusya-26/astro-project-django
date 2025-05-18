"""Space System db model is defined here."""

from django.db import models
from django.utils import timezone

from astrocat.models.users import User


class SpaceSystem(models.Model):
    """A star system, created by a user and may contain multiple space objects."""

    name = models.CharField(max_length=255, unique=True, blank=True, null=False)
    galaxy = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="space_systems")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ["id"]

    def __str__(self):
        return "<Space System> " + self.name
