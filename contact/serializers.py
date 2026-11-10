import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=80, required=False, allow_blank=True)
    email = serializers.EmailField(max_length=254)
    subject = serializers.CharField(
        max_length=120, required=False, allow_blank=True)
    message = serializers.CharField(min_length=10, max_length=5000)
    app = serializers.CharField(
        max_length=40, required=False, allow_blank=True)
    app_version = serializers.CharField(
        max_length=32, required=False, allow_blank=True)
    # Honeypot: insanlar görmez, botlar doldurur.
    website = serializers.CharField(required=False, allow_blank=True)
    captcha = serializers.CharField(
        write_only=True, required=False, allow_blank=True)

    def validate(self, attrs):
        # Honeypot dolu ise captcha doğrulanmaz; görünüm sessizce yok sayar.
        if attrs.get('website'):
            return attrs
        if settings.CONTACT_REQUIRE_CAPTCHA:
            self._verify_captcha(attrs.get('captcha', ''))
        return attrs

    @staticmethod
    def _verify_captcha(value):
        if not value:
            raise serializers.ValidationError(
                {'captcha': _('recaptcha_verification_failed')})
        response = requests.post(
            settings.RECAPTCHA_URL,
            data={'secret': settings.RECAPTCHA_SECRET_KEY, 'response': value},
            timeout=10,
        )
        if not response.json().get('success'):
            raise serializers.ValidationError(
                {'captcha': _('recaptcha_verification_failed')})
