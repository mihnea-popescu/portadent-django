from __future__ import annotations

import base64

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


def base64_to_image(image_b64: str) -> Image:
    """Convert a base64 string to an image."""
    image_format, imgstr = image_b64.split(';base64,')
    ext = image_format.split('/')[-1]
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


def image_to_base64(image: Image, img_format: str = "JPEG") -> str:
    """Convert an image to a base64 string."""
    ACCEPTED_FORMATS = ["JPEG", "PNG"]
    if img_format not in ACCEPTED_FORMATS:
        raise ValueError(f"Invalid image format: {img_format}")

    buff = BytesIO()
    image.save(buff, format=img_format)
    image_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")
    return f"data:image/{img_format.lower()};base64,{image_b64}"
