"""News form is defined here."""

from django import forms

from astrocat.models import News


class NewsForm(forms.ModelForm):
    """Form for creating or editing a news post."""

    photo = forms.ImageField(
        required=False,
        label="Изображение",
        help_text="Только файлы PNG или JPG.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:  # pylint: disable=missing-class-docstring
        model = News
        fields = ["title", "content", "photo", "is_private"]
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
            "is_private": "Сделать новость приватной",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок"}),
            "content": forms.Textarea(attrs={"class": "form-control", "placeholder": "Чем хотите поделиться?"}),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
