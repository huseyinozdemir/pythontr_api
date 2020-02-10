from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from core.models import Category, Article

from recipe import serializers


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.DestroyModelMixin
                  ):

    authentication_classes = (TokenAuthentication,)
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


class CategoryViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes_by_action = {'create': [IsAdminUser],
                                    'list': [AllowAny],
                                    'retrieve': [AllowAny]}

    def get_queryset(self):
        categories = self.request.query_params.get('search')
        queryset = self.queryset
        if categories:
            queryset = queryset.filter(name__icontains=categories)
        if self.action == 'list':
            queryset = queryset.all()
            queryset = sorted(queryset, key=lambda x: x.full_category_name)
        return queryset


class ArticlesViewSet(BaseViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes_by_action = {'list': [AllowAny],
                                    'retrieve': [AllowAny],
                                    'updated': [IsAdminUser]}

    def get_queryset(self):
        articles = self.request.query_params.get('search')
        queryset = self.queryset
        if articles:
            queryset = queryset.filter(title__icontains=articles,
                                       is_active=True,
                                       is_delete=False)
        if self.action == 'list':
            queryset = queryset.all().filter(is_active=True, is_delete=False)
            queryset = sorted(queryset, key=lambda x: x.__str__)
        return queryset


class PrivateArticlesViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'list': [IsAuthenticated],
                                    'retrieve': [IsAuthenticated],
                                    'updated': [IsAuthenticated]}

    def get_queryset(self):
        articles = self.request.query_params.get('search')
        queryset = self.queryset
        if articles:
            queryset = queryset.filter(title__icontains=articles)
        if self.action == 'list':
            queryset = queryset.all()
            queryset = sorted(queryset, key=lambda x: x.__str__)
        return queryset
