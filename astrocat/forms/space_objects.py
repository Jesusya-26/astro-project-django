"""Space Object form is defined here."""

from django import forms

from astrocat.models import SpaceObject


class SpaceObjectForm(forms.ModelForm):
    """Form for creating or editing a space object."""

    photo = forms.ImageField(
        required=False,
        label="Изображение",
        help_text="Только PNG или JPG.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    class Meta:  # pylint: disable=missing-class-docstring
        model = SpaceObject
        exclude = ["creator", "system", "created_at"]
        labels = {
            "name": "Название объекта",
            "space_type": "Тип объекта",
            "radius": "Радиус орбиты (в а.е.)",
            "period": "Период обращения (в годах)",
            "ex": "Эксцентриситет",
            "v": "Орбитальная скорость (в км/с)",
            "p": "Плотность (×10³ кг/м³)",
            "g": "Ускорение свободного падения (в м/с²)",
            "m": "Масса (относительно Земли)",
            "sputnik": "Количество спутников",
            "atmosphere": "Атмосфера",
            "about": "Описание объекта",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "space_type": forms.TextInput(attrs={"class": "form-control"}),
            "radius": forms.NumberInput(attrs={"class": "form-control", "placeholder": "в а.е."}),
            "period": forms.NumberInput(attrs={"class": "form-control", "placeholder": "в годах"}),
            "ex": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Эксцентриситет"}),
            "v": forms.NumberInput(attrs={"class": "form-control", "placeholder": "в км/с"}),
            "p": forms.NumberInput(attrs={"class": "form-control", "placeholder": "×10³ кг/м³"}),
            "g": forms.NumberInput(attrs={"class": "form-control", "placeholder": "в м/с²"}),
            "m": forms.NumberInput(attrs={"class": "form-control", "placeholder": "относительно Земли"}),
            "sputnik": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Количество спутников"}),
            "atmosphere": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Описание атмосферы",
                }
            ),
            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Общее описание объекта",
                }
            ),
        }
