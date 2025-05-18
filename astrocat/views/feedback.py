"""Views for `About` and `Feedback` page are defined here."""

from django.http.request import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from astrocat.forms import FeedbackForm


def about_view(request: HttpRequest):
    """Renders the About page."""
    return render(request, "about.html")


@require_http_methods(["GET", "POST"])
def feedback_view(request: HttpRequest):
    """Handles user feedback form:
    - On GET: displays a blank feedback form.
    - On POST: validates and saves the form data.
    """
    success = False

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = FeedbackForm()  # reset form after successful submission
    else:
        form = FeedbackForm()

    context = {
        "form": form,
        "success": success,
    }
    return render(request, "feedback.html", context)
