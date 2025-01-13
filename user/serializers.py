import sys
import requests

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    is_staff = serializers.BooleanField()
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    current_password = serializers.CharField(
        write_only=True,
        required=False,
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
                    _("recaptcha_verification_failed"))

            return value

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'password', 'confirm_password', 'username',
            'name', 'surname', 'image', 'about_me', 'linkedin',
            'github', 'is_notification_email', 'image_url', 'slug',
            'is_staff', 'current_password'
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
        if password:
            confirm_password = data.get('confirm_password')
            current_password = data.get('current_password')

            if not confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': _('please_confirm_your_password')
                })

            if password != confirm_password:
                raise serializers.ValidationError({
                    "confirm_password": _("passwords_do_not_match")
                    })

            if self.context['request'].method in ['PUT', 'PATCH']:
                if not current_password:
                    raise serializers.ValidationError({
                        'current_password': _(
                            'please_enter_your_current_password'
                        )
                    })

                user = self.context['request'].user
                if not user.check_password(current_password):
                    raise serializers.ValidationError({
                        'current_password': _('current_password_is_incorrect')
                    })

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
        if self.partial:
            validated_data.pop('confirm_password', None)
            validated_data.pop('current_password', None)
        else:
            validated_data.pop('confirm_password')
            validated_data.pop('current_password')
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
                    _("recaptcha_verification_failed"))

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
            msg = _('unable_to_authenticate_with_provided_credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

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

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": _('email_not_found')})
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField()
    uidb64 = serializers.CharField()

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

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': _('passwords_do_not_match')}
            )
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            raise serializers.ValidationError({'error': _('invalid_link')})

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError(
                {'error': _('invalid_link_or_expired')})

        data['user'] = user
        return data
