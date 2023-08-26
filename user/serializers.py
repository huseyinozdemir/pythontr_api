import sys
import requests

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
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
                    _("reCAPTCHA verification failed"))

            return value

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'password', 'confirm_password', 'username',
            'name', 'surname', 'image', 'about_me', 'linkedin',
            'is_notification_email', 'image_url', 'slug'
        ]
        if not settings.DEBUG and 'test' not in sys.argv:
            fields.append('captcha')

        read_only_fields = ('id', 'slug')
        extra_kwargs = {
            'password': {
                'write_only': True, 'min_length': 5,
                'style': {'input_type': 'password'}}}

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(_("Passwords do not match"))

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        return get_user_model().objects.create_user(
            password=password,
            **validated_data
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password')
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

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
                    _("reCAPTCHA verification failed"))

            return value

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
