from rest_framework import mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext as _

from core.models import Slider

from recipe import serializers
from recipe.permissions import IsAuthenticatedAndOwner

from .baseview import BaseViewSet
from .filter_param import RulesFilter, Search, Me


class SliderViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Slider.objects.select_related('user').all()
    serializer_class = serializers.SliderSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticated],
        'update': [IsAuthenticatedAndOwner],
    }

    def get_object(self):
        id = self.kwargs.get('pk')
        return Slider.objects.get(pk=id)

    def get_queryset(self):
        """ self.action == 'list' """
        search = self.request.query_params.get('search', None)
        me = self.request.query_params.get('me', None)
        queryset = None

        SearchKwargs = {
            '{0}__{1}'.format('title', 'icontains'): search,
        }

        MeKwargs = {
            '{0}'.format('user'): self.request.user,
        }

        rules = [
            Search(search, **SearchKwargs),
            Me(me, **MeKwargs)
        ]

        kwargs = {
            '{0}_{1}'.format('is', 'active'): True,
            '{0}_{1}'.format('is', 'delete'): False,
        }

        rf = RulesFilter(rules)
        for item in rf.get_res():
            if item.is_check():
                kwargs.update(item.get_param())

        queryset = self.queryset.filter(
            **kwargs
        ).all().order_by('-id').distinct()

        if not queryset.exists():
            raise NotFound(_('not_found'))

        return queryset
