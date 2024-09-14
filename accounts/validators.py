from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    # Get file extension
    ext = os.path.splitext(value.name)[1].lower()  # Convert to lowercase for comparison
    valid_extensions = ['.png', '.jpg', '.jpeg']

    # Check extension
    if ext not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}'
        )

    # Optional: check MIME type (requires python-magic library)
    if not value.content_type.startswith('image'):
         raise ValidationError('File is not an image.')
