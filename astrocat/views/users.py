"""Views for users management pages are defined here."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from astrocat.forms import EditUserForm, LoginForm, RegisterForm
from astrocat.models import User
from astrocat.utils.minio import get_presigned_url_from_minio


def user_profile_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """Display user profile and associated news with MinIO image URLs."""
    user = get_object_or_404(User, id=user_id)
    news = user.news.all()

    for item in news:
        # Attach presigned MinIO URL to each news item
        item.minio_url = get_presigned_url_from_minio(f"news/{item.id}.png")

    return render(
        request,
        "user_profile.html",
        {
            "title": "Профиль",
            "current_user": user,
            "news": news,
        },
    )


def register_view(request: HttpRequest) -> HttpResponse:
    """Handle user registration.
    - GET: Show empty registration form.
    - POST: Validate form, create user, log in and redirect.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Validate password match
            if data["password"] != data["password_again"]:
                return render(
                    request,
                    "register.html",
                    {"form": form, "message": "Пароли не совпадают!"},
                )

            # Check email and username uniqueness
            if User.objects.filter(email=data["email"]).exists():
                return render(
                    request,
                    "register.html",
                    {"form": form, "message": "Такой пользователь уже есть!"},
                )

            if User.objects.filter(username=data["username"]).exists():
                return render(
                    request,
                    "register.html",
                    {"form": form, "message": "Логин занят!"},
                )

            # Create and login new user
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                name=data["name"],
                surname=data["surname"],
                age=data["age"],
                about=data["about"],
            )
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    """Handle user login.
    - GET: Show login form.
    - POST: Authenticate user, login and redirect.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)

                # Optionally disable session persistence
                if not form.cleaned_data.get("remember_me"):
                    request.session.set_expiry(0)

                return redirect("/")
            return render(
                request,
                "login.html",
                {"form": form, "message": "Неправильный логин или пароль"},
            )
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """Log out the current user and redirect to home page."""
    logout(request)
    return redirect("/")


@login_required
def edit_user_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """Allow the user to edit their profile.
    - GET: Show form pre-filled with user data.
    - POST: Validate and save changes.
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            new_username = form.cleaned_data["username"]

            # Check for username conflicts
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                return render(
                    request,
                    "user.html",
                    {"form": form, "message": "Логин занят!"},
                )

            form.save()
            return redirect("user_profile", user_id=user.id)
    else:
        form = EditUserForm(instance=user)

    return render(request, "user.html", {"form": form})
