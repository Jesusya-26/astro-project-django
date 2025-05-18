"""Models registration is defined here."""

from django.contrib import admin

from astrocat import models

admin.site.register(models.Feedback)
admin.site.register(models.News)
admin.site.register(models.SpaceObject)
admin.site.register(models.SpaceSystem)
admin.site.register(models.User)
