from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    create_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    ip = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    comments = GenericRelation('self')

    def __str__(self):
        return self.content
