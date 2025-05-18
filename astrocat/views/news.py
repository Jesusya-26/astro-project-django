"""Views for main and news management pages are defined here."""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from astrocat.forms import NewsForm
from astrocat.models import News
from astrocat.utils.minio import (
    delete_image_from_minio,
    get_presigned_url_from_minio,
    put_image_to_minio,
)


def main_page_view(request: HttpRequest) -> HttpResponse:
    """Render the main page with news list:
    - Superusers see all news.
    - Authenticated users see their own and public news.
    - Anonymous users see only public news.

    Each news item is supplemented with a presigned image URL from MinIO.
    """
    if request.user.is_superuser:
        news_queryset = News.objects.all()  # pylint: disable=no-member
    elif request.user.is_authenticated:
        news_queryset = News.objects.filter(Q(user=request.user) | Q(is_private=False))  # pylint: disable=no-member
    else:
        news_queryset = News.objects.filter(is_private=False)  # pylint: disable=no-member

    # Attach presigned image URLs to news items
    for news in news_queryset:
        news.minio_url = get_presigned_url_from_minio(f"news/{news.id}.png")

    context = {
        "title": "AstroCat",
        "news": news_queryset,
    }
    return render(request, "main_page.html", context)


@login_required
def add_news_view(request: HttpRequest) -> HttpResponse:
    """Handle the creation of a new news item.
    - On GET: renders a blank form.
    - On POST: saves the form and uploads the image to MinIO if present.
    """
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user
            news.save()

            if "photo" in request.FILES:
                photo = request.FILES["photo"]
                filename = f"news/{news.id}.png"
                put_image_to_minio(photo, filename)

            return redirect("home")
    else:
        form = NewsForm()

    return render(request, "news.html", {"form": form})


@login_required
def edit_news_view(request: HttpRequest, news_id: int) -> HttpResponse:
    """Edit an existing news item.
    - On GET: shows the form with current data.
    - On POST: updates the news and replaces the image if uploaded.
    """
    news = get_object_or_404(News, id=news_id)
    filename = f"news/{news.id}.png"

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            if "photo" in request.FILES:
                put_image_to_minio(request.FILES["photo"], filename)
            form.save()
            return redirect("home")
    else:
        form = NewsForm(instance=news)

    photo_url = get_presigned_url_from_minio(filename)
    return render(request, "news.html", {"form": form, "photo": photo_url})


@login_required
def delete_news_view(request: HttpRequest, news_id: int) -> HttpResponse:  # pylint: disable=unused-argument
    """Delete a news item and its associated image from MinIO storage."""
    news = get_object_or_404(News, id=news_id)
    filename = f"news/{news.id}.png"
    delete_image_from_minio(filename)
    news.delete()
    return redirect("home")
