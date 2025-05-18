"""Space Object db model is defined here."""

from django.db import models
from django.utils import timezone

from astrocat.models.space_systems import SpaceSystem
from astrocat.models.users import User


class SpaceObject(models.Model):
    """A celestial object that belongs to a space system."""

    name = models.CharField(max_length=255, unique=True, blank=True, null=False)
    space_type = models.CharField(max_length=255, blank=True, null=True)
    radius = models.FloatField(blank=True, null=True)
    period = models.FloatField(blank=True, null=True)
    ex = models.FloatField(blank=True, null=True)
    v = models.FloatField(blank=True, null=True)
    p = models.FloatField(blank=True, null=True)
    g = models.FloatField(blank=True, null=True)
    m = models.FloatField(blank=True, null=True)
    sputnik = models.IntegerField(blank=True, null=True)
    atmosphere = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    system = models.ForeignKey(SpaceSystem, on_delete=models.CASCADE, related_name="space_objects")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="space_objects")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:  # pylint: disable=missing-class-docstring
        ordering = ["id"]

    def __str__(self):
        return "<Space Object> " + self.name
