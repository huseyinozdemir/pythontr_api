from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


from core.models import Category

from recipe import serializers


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                      mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    permission_classes_by_action = {'create': [IsAdminUser],
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

    def get_queryset(self):
        categories = self.queryset.all()
        categories = sorted(categories, key=lambda x: x.__str__())
        for cat in categories:
            cat.name = cat.__str__()
        return categories

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
