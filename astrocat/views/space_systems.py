"""Views for space systems management pages are defined here."""

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from astrocat.forms import SpaceSystemForm
from astrocat.models import SpaceSystem
from astrocat.utils.minio import delete_image_from_minio, download_file_from_minio


def data_page_view(request: HttpRequest) -> HttpResponse:
    """Display the main data page containing all space systems except the solar system, which is shown separately."""
    solar_system = get_object_or_404(SpaceSystem, name="Солнечная система")
    systems = SpaceSystem.objects.exclude(name="Солнечная система")  # pylint: disable=no-member

    # Annotate each system with a flag indicating whether the current user is its owner
    for system in systems:
        system.is_owner = request.user == system.creator or request.user.is_superuser

    context = {
        "title": "AstroCat",
        "solar_system": solar_system,
        "systems": systems,
    }
    return render(request, "data_page.html", context)


@login_required
def add_system_view(request: HttpRequest) -> HttpResponse:
    """View for creating a new space system.
    - GET: renders the form.
    - POST: validates and saves the system.
    """
    if request.method == "POST":
        form = SpaceSystemForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            system.creator = request.user
            system.save()
            return redirect("database")
    else:
        form = SpaceSystemForm()

    return render(request, "space_system.html", {"form": form})


@login_required
def edit_system_view(request: HttpRequest, system_id: int) -> HttpResponse:
    """View for editing an existing space system.
    - GET: renders form with existing data.
    - POST: validates and updates system.
    """
    system = get_object_or_404(SpaceSystem, id=system_id)

    if request.method == "POST":
        form = SpaceSystemForm(request.POST, instance=system)
        if form.is_valid():
            form.save()
            return redirect("database")
    else:
        form = SpaceSystemForm(instance=system)

    return render(request, "space_system.html", {"form": form})


@login_required
def delete_system_view(request: HttpRequest, system_id: int) -> HttpResponse:  # pylint: disable=unused-argument
    """Delete a space system and all its related space object images from MinIO."""
    system = get_object_or_404(SpaceSystem, id=system_id)

    # Delete each associated object's image from MinIO
    for space_object in system.space_objects.all():
        delete_image_from_minio(f"space_objects/{space_object.id}.png")

    system.delete()
    return redirect("database")


def download_solar_system_view(request: HttpRequest) -> FileResponse:  # pylint: disable=unused-argument
    """Download the precompiled solar system model executable.

    Returns 404 if the file is not found in MinIO."""
    filename = "modelSolarSystem.exe"

    try:
        file_obj = download_file_from_minio(filename)
    except Exception as exc:
        raise Http404("Requested file was not found in storage.") from exc

    response = FileResponse(
        file_obj,
        content_type="application/vnd.microsoft.portable-executable",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
