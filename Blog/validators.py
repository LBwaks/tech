from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:
        raise ValidationError(_("Photo should be less than 5mbs"), code="invalid")
    else:
        return value
