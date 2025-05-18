"""Feedback form is defined here."""

from django import forms

from astrocat.models import Feedback


class FeedbackForm(forms.ModelForm):
    """Form for saving user's feedback."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = Feedback
        fields = ["name", "email", "message"]
        labels = {
            "name": "Имя",
            "email": "Электронная почта",
            "message": "Сообщение",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Как вас зовут?"}),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите адрес электронной почты",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Расскажите нам, что вас волнует",
                    "rows": 4,
                }
            ),
        }
