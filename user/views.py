
from smtplib import SMTPException
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from app.authentication import CookieTokenAuthentication
from user.serializers import UserSerializer, AuthTokenSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer, \
    ResendActivationSerializer
from core.models import ActivationCode

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        activation = ActivationCode.create_activation_code(user)
        try:
            send_mail(
                _('welcome_to_www'),
                _('welcome_to_www_message').format(
                    link=f'{settings.SITE_URL}/register/activate/'
                         f'{activation.code}',
                    expires_at=activation.expires_at.strftime("%d/%m/%Y %H:%M")
                ),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except SMTPException as e:
            return Response(
                {'error': _('error_sending_email'), 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,
                              CookieTokenAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ActivateUserView(generics.GenericAPIView):
    def get(self, request, code):
        try:
            activation = ActivationCode.objects.get(
                code=code,
                is_used=False
            )

            if activation.is_expired:
                return Response(
                    {'error': _('activation_code_is_expired')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = activation.user
            user.is_active = True
            user.save()

            activation.is_used = True
            activation.save()

            return Response(
                {'message': _('account_activated_successfully')},
                status=status.HTTP_200_OK
            )

        except ActivationCode.DoesNotExist:
            return Response(
                {'error': _('activation_code_is_invalid')},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResendActivationView(generics.GenericAPIView):
    serializer_class = ResendActivationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=False)
            activation = ActivationCode.create_activation_code(user)

            send_mail(
                _('new_activation_code_title'),
                _('new_activation_code_message').format(
                    link=f'{settings.SITE_URL}/register/activate/'
                         f'{activation.code}',
                    expires_at=activation.expires_at.strftime("%d/%m/%Y %H:%M")
                ),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {'message': _('new_activation_code_sent')},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'error': _('user_not_found_with_active_code')},
                status=status.HTTP_400_BAD_REQUEST
            )
        except SMTPException as e:
            return Response(
                {'error': _('error_sending_email'), 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Token and UID
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Send Email
        try:
            reset_url = f"{settings.SITE_URL}/forgot-password/{uidb64}/{token}"
            send_mail(
                _('password_reset_title'),
                _('password_reset_message').format(link=reset_url),
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except SMTPException as e:
            return Response(
                {'error': _('error_sending_email'), 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': _('password_reset_success_message_link_sent')
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, uidb64, token):
        try:
            # Check Token and UID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {'error': _('invalid_token_or_expired')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({'valid': True})

        except (TypeError, ValueError, User.DoesNotExist):
            return Response(
                {'error': _('invalid_link')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        password = serializer.validated_data['password']

        user.set_password(password)
        user.save()

        return Response({
            'message': _('password_reset_success_message')
        })
