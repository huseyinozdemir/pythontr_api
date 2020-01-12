from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


from core.models import Category

from recipe import serializers


class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(BaseViewSet):

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        categories = self.queryset.all()
        #categories = sorted(categories, key=lambda x: x.__str__())
        categories = sorted(categories, key=lambda x: x.full_category_name)
        return categories
