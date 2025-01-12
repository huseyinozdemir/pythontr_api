import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta

User = get_user_model()


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        now = timezone.now()
        expires_at = self.expires_at
        if self.expires_at.tzinfo is None:
            expires_at = timezone.make_aware(self.expires_at)
        return now > expires_at

    @classmethod
    def create_activation_code(cls, user):
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        return cls.objects.create(user=user)
