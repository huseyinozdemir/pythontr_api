from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings

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

    def __str__(self):
        return self.title
