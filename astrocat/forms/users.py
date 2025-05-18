"""User forms for registration, login and editing are defined here."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from astrocat.models import User


class RegisterForm(forms.ModelForm):
    """Form for user registration."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Пароль",
        help_text="Введите надежный пароль",
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Повторите пароль",
        help_text="Введите пароль ещё раз для проверки",
    )

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = ["username", "name", "surname", "email", "age", "about"]
        labels = {
            "username": "Имя пользователя",
            "name": "Имя",
            "surname": "Фамилия",
            "email": "Электронная почта",
            "age": "Возраст",
            "about": "О себе",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "about": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get("password")
        pwd2 = cleaned_data.get("password_again")
        if pwd and pwd != pwd2:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data


class LoginForm(AuthenticationForm):
    """Form for user authentication."""

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="Запомнить меня",
    )


class EditUserForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = ["username", "name", "surname", "age", "about"]
        labels = {
            "username": "Имя пользователя",
            "name": "Имя",
            "surname": "Фамилия",
            "age": "Возраст",
            "about": "О себе",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
