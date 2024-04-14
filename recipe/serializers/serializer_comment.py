import sys
import requests

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


from core.models import Comment


class CommentReleatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'email',
            'name',
            'ip',
            'user',
            'content_type',
            'object_id',
        )


class CommentSerializer(serializers.ModelSerializer):
    comments = CommentReleatedSerializer(many=True, required=False,
                                         read_only=True)

    if not settings.DEBUG and 'test' not in sys.argv:
        captcha = serializers.CharField(write_only=True, required=True)

        def validate_captcha(self, value):
            recaptcha_url = settings.RECAPTCHA_URL
            payload = {
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": value
            }
            response = requests.post(recaptcha_url, data=payload)
            result = response.json()

            if not result.get("success"):
                raise serializers.ValidationError(
                    _("recaptcha_verification_failed"))

            return value

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'email',
            'name',
            'ip',
            'user',
            'content_type',
            'object_id',
            'comments',
        ]
        if not settings.DEBUG and 'test' not in sys.argv:
            fields.append('captcha')
