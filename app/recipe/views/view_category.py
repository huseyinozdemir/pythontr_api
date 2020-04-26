from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser

from core.models import Category

from recipe import serializers

from .baseview import BaseViewSet
from .filter_param import RulesFilter, Search


class CategoryViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes_by_action = {'create': [IsAdminUser],
                                    'list': [AllowAny],
                                    'retrieve': [AllowAny]}

    def get_queryset(self):
        search = self.request.query_params.get('search')
        queryset = None

        SearchKwargs = {
            '{0}__{1}'.format('name', 'icontains'): search,
        }

        rules = [
            Search(search, **SearchKwargs),
        ]

        kwargs = {}

        rf = RulesFilter(rules)

        for item in rf.get_res():
            if item.is_check():
                kwargs.update(item.get_param())

        queryset = self.queryset.filter(**kwargs).all()
        queryset = sorted(queryset, key=lambda x: x.full_category_name)
        return queryset
