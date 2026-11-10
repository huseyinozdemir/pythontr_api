import logging
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from contact.serializers import ContactSerializer

logger = logging.getLogger(__name__)


def _one_line(value):
    """Başlık alanlarında satır sonu kullanılamaz (header injection)."""
    return ' '.join(str(value).split())


class ContactView(generics.GenericAPIView):
    """Destek formu: mesajı site sahibine e-postayla iletir.

    Gönderenin adresi Reply-To'ya konur; adres hiçbir yerde saklanmaz.
    """
    serializer_class = ContactSerializer
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'contact'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data.get('website'):
            # Bot: başarılıymış gibi davran, gönderme.
            return Response({'sent': True},
                            status=status.HTTP_200_OK)

        app = _one_line(data.get('app', '')) or 'Contact'
        subject = _one_line(data.get('subject', '')) or '(no subject)'
        name = _one_line(data.get('name', ''))
        sender = _one_line(data['email'])
        body = (
            f'From: {name} <{sender}>\n' if name else f'From: {sender}\n'
        ) + (
            f'App: {app} {_one_line(data.get("app_version", ""))}\n'
        ) + f'\n{data["message"]}\n'

        try:
            EmailMessage(
                subject=f'[{app}] {subject}',
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[sender],
            ).send(fail_silently=False)
        except (SMTPException, OSError):
            logger.exception('contact mail could not be sent')
            return Response({'error': _('error_sending_email')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'sent': True},
                        status=status.HTTP_200_OK)
