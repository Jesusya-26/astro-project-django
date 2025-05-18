"""Space System form is defined here."""

from django import forms

from astrocat.models import SpaceSystem


class SpaceSystemForm(forms.ModelForm):
    """Form for creating or editing a star system."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = SpaceSystem
        exclude = ["creator", "created_at"]
        labels = {
            "name": "Название системы",
            "galaxy": "Галактика",
            "about": "Описание системы",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название системы"}),
            "galaxy": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название галактики"}),
            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Общее описание системы",
                }
            ),
        }
