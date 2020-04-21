from django.db import models

from django.conf import settings


class InboxManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=0)


class Inbox(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender_user',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reciever_user',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    subject = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    ip = models.CharField(max_length=100, blank=False)

    is_delete = models.BooleanField(default=False)

    objects = InboxManager()

    def __str__(self):
        return self.subject
