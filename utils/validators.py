import os
from django.core.exceptions import ValidationError
from utils.constants import POST_DOCUMENT_ALLOWED_EXTS


def post_document_size(value):

    if value.size >  2 * 1024 * 1024*1024*1024:
        raise ValidationError('invalid file size')


def post_document_extension(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in POST_DOCUMENT_ALLOWED_EXTS:
        raise ValidationError(f'not allowed ext, allowed ({POST_DOCUMENT_ALLOWED_EXTS})')