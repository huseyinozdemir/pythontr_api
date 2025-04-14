import sys
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
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

    def get_comments(self, obj):
        comments = Comment.objects.filter(
            content_type__model='comment',
            object_id=obj.id
        )

        serializer = CommentSerializer(
            comments,
            many=True,
            context=self.context
        )
        return serializer.data

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
