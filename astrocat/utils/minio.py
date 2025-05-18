"""
MinIO utility functions for working with media files in the Astro Project.

This module provides helper functions for:
- Generating presigned download URLs
- Uploading converted images to MinIO
- Downloading and deleting objects from MinIO
- Converting images to a PNG format with compression and resizing

Dependencies:
- MinIO SDK for Python
- Pillow for image processing
"""

import io

from minio import Minio
from minio.error import S3Error
from PIL import Image

from astro_project import settings


def _get_minio_client() -> Minio:
    """Create and return a configured MinIO client instance."""
    return Minio(
        endpoint=f"{settings.MINIO_CONF['HOST']}:{settings.MINIO_CONF['PORT']}",
        access_key=settings.MINIO_CONF["ACCESS_KEY"],
        secret_key=settings.MINIO_CONF["SECRET_KEY"],
        secure=False,
    )


def get_presigned_url_from_minio(filename: str) -> str | None:
    """
    Generate a presigned URL for downloading an object from MinIO.

    Args:
        filename (str): Name of the file in the bucket.

    Returns:
        Optional[str]: Presigned URL if file exists, otherwise None.
    """
    client = _get_minio_client()
    try:
        client.stat_object(
            bucket_name=settings.MINIO_CONF["BUCKET"],
            object_name=filename,
        )
        return client.presigned_get_object(
            bucket_name=settings.MINIO_CONF["BUCKET"],
            object_name=filename,
        )
    except S3Error:
        return None


def put_image_to_minio(photo, filename: str) -> None:
    """
    Convert and upload an image to MinIO as PNG.

    Args:
        photo (InMemoryUploadedFile): Uploaded photo from a Django form.
        filename (str): Target filename in the bucket.
    """
    client = _get_minio_client()
    converted = convert_image_to_png(photo.file)

    # Get size of the stream
    converted.seek(0, io.SEEK_END)
    size = converted.tell()
    converted.seek(0)

    client.put_object(
        bucket_name=settings.MINIO_CONF["BUCKET"],
        object_name=filename,
        data=converted,
        length=size,
        content_type="image/png",
    )


def download_file_from_minio(filename: str):
    """
    Download a file object from MinIO.

    Args:
        filename (str): Name of the file to download.

    Returns:
        HTTPResponse: File-like object from MinIO.
    """
    client = _get_minio_client()
    return client.get_object(
        bucket_name=settings.MINIO_CONF["BUCKET"],
        object_name=filename,
    )


def delete_image_from_minio(filename: str) -> None:
    """
    Delete an object from MinIO.

    Args:
        filename (str): Name of the object to delete.
    """
    client = _get_minio_client()
    client.remove_object(
        bucket_name=settings.MINIO_CONF["BUCKET"],
        object_name=filename,
    )


def convert_image_to_png(  # pylint: disable=missing-param-doc,missing-type-doc
    image_file, max_dimension: int = 1200, quality: int = 85
) -> io.BytesIO:
    """
    Convert and resize an image file to PNG format.

    Args:
        image_file (file-like): Input image file.
        max_dimension (int): Maximum width or height in pixels.
        quality (int): Output quality (for lossy compression compatibility).

    Returns:
        io.BytesIO: Converted image in a BytesIO stream.
    """
    try:
        image = Image.open(image_file)
    except Exception as exc:
        raise ValueError("Invalid image passed") from exc

    # Convert non-RGB images to RGBA (PNG-compatible)
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    resized_image = image.copy()

    # Resize image if it exceeds max dimension
    width, height = image.size
    if width > max_dimension or height > max_dimension:
        ratio = min(max_dimension / width, max_dimension / height)
        new_size = (int(width * ratio), int(height * ratio))
        resized_image = resized_image.resize(new_size, Image.Resampling.LANCZOS)

    output_stream = io.BytesIO()
    resized_image.save(output_stream, format="PNG", quality=quality)
    output_stream.seek(0)

    return output_stream
