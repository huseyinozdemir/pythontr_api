from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from app.authentication import CookieTokenAuthentication
from user.serializers import UserSerializer, AuthTokenSerializer
from core.models import ActivationCode

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        activation = ActivationCode.create_activation_code(user)
        send_mail(
            'Pythontr.com sitemize hoşgeldiniz!',
            'Hesabınızı aktif hale getirmek için lütfen aşağıdaki linki '
            'tıklayınız.\n'
            f'{settings.SITE_URL}/register/activate/{activation.code}\n\n'
            f'Bu link {activation.expires_at.strftime("%d/%m/%Y %H:%M")}'
            ' tarihine kadar geçerlidir.\n\n'
            'Pythontr.com Team',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
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
                    {'error': 'Aktivasyon kodunun süresi dolmuş.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = activation.user
            user.is_active = True
            user.save()

            activation.is_used = True
            activation.save()

            return Response({'message': 'Hesabınız başarıyla aktive edildi.'})

        except ActivationCode.DoesNotExist:
            return Response(
                {'error': 'Geçersiz aktivasyon kodu.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResendActivationView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_active=False)
            activation = ActivationCode.create_activation_code(user)

            send_mail(
                'Yeni Aktivasyon Kodu',
                'Yeni aktivasyon kodunuz: '
                f'{settings.SITE_URL}/register/activate/{activation.code}\n'
                f'Bu link {activation.expires_at.strftime("%d/%m/%Y %H:%M")}'
                ' tarihine kadar geçerlidir.\n\n'
                'Pythontr.com Team',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {'message':
                 'Yeni aktivasyon kodu email adresinize gönderildi.'},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {'error': 'Bu email adresi ile kayıtlı '
                          'aktif edilmemiş hesap bulunamadı.'},
                status=status.HTTP_400_BAD_REQUEST
            )
