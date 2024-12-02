from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User


class CookieTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('token')
        if not token:
            return None

        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            raise AuthenticationFailed('Geçersiz token.')

        return (user, token)
