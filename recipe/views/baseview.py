from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from app.authentication import CookieTokenAuthentication


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin
                  ):

    authentication_classes = (TokenAuthentication, CookieTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    permission_classes_by_action = {'update': [IsAdminUser],
                                    'retrieve': [AllowAny],
                                    'list': [AllowAny]}

    def get_permissions(self):
        try:
            result = None
            permission_list = []
            for permission in self.permission_classes_by_action[self.action]:
                permission_list.append(permission())
            result = permission_list
        except KeyError:
            result = [permission() for permission in self.permission_classes]
        finally:
            return result

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
