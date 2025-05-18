"""Views for space objects management pages are defined here."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from astrocat.forms import SpaceObjectForm
from astrocat.models import SpaceObject, SpaceSystem
from astrocat.utils.minio import (
    delete_image_from_minio,
    get_presigned_url_from_minio,
    put_image_to_minio,
)


def space_object_detail_view(request: HttpRequest, object_id: int) -> HttpResponse:
    """Render the details of a space object with an associated image from MinIO."""
    space_object = get_object_or_404(SpaceObject, id=object_id)
    photo_url = get_presigned_url_from_minio(f"space_objects/{space_object.id}.png")

    context = {
        "title": space_object.name,
        "space_object": space_object,
        "photo": photo_url,
    }
    return render(request, "space_object_info.html", context)


@login_required
def add_space_object_view(request: HttpRequest, system_id: int) -> HttpResponse:
    """Handle creation of a new space object.
    - GET: renders the form.
    - POST: processes form data and uploads image to MinIO.
    """
    system = get_object_or_404(SpaceSystem, id=system_id)

    if request.method == "POST":
        form = SpaceObjectForm(request.POST, request.FILES)
        if form.is_valid():
            space_object = form.save(commit=False)
            space_object.system = system
            space_object.creator = request.user
            space_object.save()  # Save before uploading photo to get an ID

            # Upload photo to MinIO if present
            if "photo" in request.FILES:
                photo = request.FILES["photo"]
                filename = f"space_objects/{space_object.id}.png"
                put_image_to_minio(photo, filename)

            return redirect("space_object_info", object_id=space_object.id)
    else:
        form = SpaceObjectForm()

    return render(request, "space_object.html", {"form": form})


@login_required
def edit_space_object_view(request: HttpRequest, object_id: int) -> HttpResponse:
    """Edit an existing space object.
    - GET: prepopulate form with existing data.
    - POST: update object and replace image if new photo is uploaded.
    """
    space_object = get_object_or_404(SpaceObject, id=object_id)
    filename = f"space_objects/{space_object.id}.png"

    if request.method == "POST":
        form = SpaceObjectForm(request.POST, request.FILES, instance=space_object)
        if form.is_valid():
            # Replace image in MinIO if new one provided
            if "photo" in request.FILES:
                put_image_to_minio(request.FILES["photo"], filename)
            form.save()
            return redirect("space_object_info", object_id=space_object.id)
    else:
        form = SpaceObjectForm(instance=space_object)

    photo_url = get_presigned_url_from_minio(filename)
    return render(request, "space_object.html", {"form": form, "photo": photo_url})


@login_required
def delete_space_object_view(request: HttpRequest, object_id: int) -> HttpResponse:  # pylint: disable=unused-argument
    """Delete a space object and its corresponding image from MinIO."""
    space_object = get_object_or_404(SpaceObject, id=object_id)
    filename = f"space_objects/{space_object.id}.png"
    delete_image_from_minio(filename)
    space_object.delete()
    return redirect("database")
