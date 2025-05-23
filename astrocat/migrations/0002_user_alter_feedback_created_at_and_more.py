# Generated by Django 5.2.1 on 2025-05-09 09:14
# pylint: disable=missing-module-docstring,missing-class-docstring
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrocat", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                ("name", models.CharField(blank=True, max_length=150, null=True)),
                ("surname", models.CharField(blank=True, max_length=150, null=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "hashed_password",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="feedback",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="message",
            field=models.TextField(verbose_name="message content"),
        ),
        migrations.CreateModel(
            name="SpaceSystem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, unique=True)),
                ("galaxy", models.CharField(blank=True, max_length=255, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="space_systems",
                        to="astrocat.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpaceObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, unique=True)),
                ("space_type", models.CharField(blank=True, max_length=255, null=True)),
                ("radius", models.IntegerField(blank=True, null=True)),
                ("period", models.IntegerField(blank=True, null=True)),
                ("ex", models.IntegerField(blank=True, null=True)),
                ("v", models.IntegerField(blank=True, null=True)),
                ("p", models.IntegerField(blank=True, null=True)),
                ("g", models.IntegerField(blank=True, null=True)),
                ("m", models.IntegerField(blank=True, null=True)),
                ("sputnik", models.IntegerField(blank=True, null=True)),
                ("atmosphere", models.TextField(blank=True, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "system",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="space_objects",
                        to="astrocat.spacesystem",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="space_objects",
                        to="astrocat.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255)),
                ("content", models.TextField(blank=True, null=True)),
                ("is_private", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="news",
                        to="astrocat.user",
                    ),
                ),
            ],
        ),
    ]
