import base64
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


def decode_base64_to_image(b64_string: str) -> Image:
    """Convert a base64-encoded string into an image object."""
    img_format, encoded_data = b64_string.split(';base64,')
    file_extension = img_format.split('/')[-1]
    return ContentFile(base64.b64decode(encoded_data), name=f"temp.{file_extension}")


def encode_image_to_base64(image: Image, format: str = "JPEG") -> str:
    """Convert an image object into a base64-encoded string."""
    SUPPORTED_FORMATS = ["JPEG", "PNG"]
    if format not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {format}")

    buffer = BytesIO()
    image.save(buffer, format=format)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{encoded_image}"
