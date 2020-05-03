from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings

from django.utils import timezone
from django.utils.text import slugify

from .model_category import Category
from .model_comment import Comment


class Article(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(
        Category,
        related_name='article',
    )
    title = models.CharField(max_length=255, unique=True)
    title_h1 = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
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

        return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
