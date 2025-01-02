import os
import shutil

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings

from django.utils import timezone
from django.utils.text import slugify

from .model_category import Category
from .model_comment import Comment


def article_image_file_path(instance, filename):
    f_name, ext = filename.split('.')
    allowed_chars = \
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
    sanitized_filename = ''.join(
        c for c in f_name if c in allowed_chars).strip()
    slug = slugify(sanitized_filename)
    folder = instance.pk if instance.pk else 'temp'
    file_path = f'{settings.ARTICLE_ROOT}{folder}/{slug}.{ext}'
    return file_path


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category,
        related_name='article',
    )
    title = models.CharField(max_length=255, unique=True)
    title_h1 = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=article_image_file_path,
                              blank=True)
    comments = GenericRelation(Comment)
    read_count = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    is_approval = models.BooleanField(default=False)
    approval_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='approval_user',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_delete = models.BooleanField(default=False)

    def get_slug(self):
        slug = slugify(self.title_h1.replace('ı', 'i'))
        unique = slug
        number = 1

        while Article.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.title_h1:
            self.title_h1 = self.title

        self.updated_at = timezone.now()
        self.slug = self.get_slug()

        super(Article, self).save(*args, **kwargs)
        if self.image and 'temp' in self.image.path:
            filename = os.path.basename(self.image.name).strip()
            new_path = f'{settings.ARTICLE_ROOT}{self.pk}/{filename}'
            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            old_path = self.image.path
            self.image.name = new_path
            super(Article, self).save(update_fields=['image'])

            if os.path.exists(old_path):
                shutil.move(old_path, new_path)

        return self

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        image_url = None
        if self.image:
            image_url = self.image.url.replace(settings.APLICATION_NAME, '')
        return image_url
