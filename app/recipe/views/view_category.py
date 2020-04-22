from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser

from core.models import Category

from recipe import serializers

from .baseview import BaseViewSet


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
