from django.db import models
from django.conf import settings
from django.utils.text import slugify


def slider_image_file_path(instance, filename):
    f_name, ext = filename.split('.')
    allowed_chars = \
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
    sanitized_filename = ''.join(c for c in f_name if c in allowed_chars)
    slug = slugify(sanitized_filename)
    file_path = f'{settings.IMAGE_ROOT}/{slug}.{ext}'
    return file_path


class Slider(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, upload_to=slider_image_file_path,
                              blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    is_approval = models.BooleanField(default=False)
    approval_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='approved_sliders',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        image_url = None
        if self.image:
            image_url = self.image.url.replace(settings.APLICATION_NAME, '')
        return image_url
