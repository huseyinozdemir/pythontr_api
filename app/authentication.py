from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import json
from urllib.parse import unquote


class CookieTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token_data = request.COOKIES.get('session')
        if not token_data:
            return None
        try:
            decoded_data = unquote(token_data)
            token = json.loads(decoded_data).get('token')
            if not token:
                return None
            if not isinstance(token, str):
                raise AuthenticationFailed('Geçersiz token formatı.')
            user = User.objects.get(auth_token=token)
            if not user.is_active:
                raise AuthenticationFailed('Kullanıcı hesabı aktif değil.')
            return (user, token)
        except (json.JSONDecodeError, AttributeError):
            return None
        except User.DoesNotExist:
            raise AuthenticationFailed('Geçersiz token.')
