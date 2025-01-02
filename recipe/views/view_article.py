from rest_framework import mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import NotFound
from django.utils.translation import gettext as _

from core.models import Article

from recipe import serializers
from recipe.permissions import IsAuthenticatedAndOwner, \
    IsAuthenticatedAndOwnerOrAdmin

from .baseview import BaseViewSet
from .filter_param import RulesFilter, Search, Me, Category


class ArticleViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Article.objects.select_related('user').all()
    serializer_class = serializers.ArticleSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticated],
        'update': [IsAuthenticatedAndOwner],
        'destroy': [IsAuthenticatedAndOwnerOrAdmin],
    }

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        id_or_slug = self.kwargs.get('pk')
        if id_or_slug.isdigit():
            return Article.objects.get(pk=id_or_slug)
        return Article.objects.get(slug=id_or_slug)

    def get_queryset(self):
        """ self.action == 'list' """
        search = self.request.query_params.get('search', None)
        categories = self.request.query_params.getlist('category', [])
        is_active = self.request.query_params.get('is_active', None)
        me = self.request.query_params.get('me', None)
        queryset = None
        self.serializer_class = serializers.ArticleListSerializer

        SearchKwargs = {
            '{0}__{1}'.format('title', 'icontains'): search,
        }
        if categories:
            SearchKwargs['{0}__{1}'.format(
                'categories__id', 'in')] = categories

        MeKwargs = {
            '{0}'.format('user'): self.request.user,
            # **({'is_active': is_active == "true"} if is_active else {})
        }

        if is_active is not None:
            if is_active in ["true", "false"]:
                MeKwargs['is_active'] = is_active.lower() == "true"

        rules = [
            Search(search, **SearchKwargs),
            Category(categories, **SearchKwargs),
            Me(me, **MeKwargs)
        ]

        kwargs = {}

        if not me:
            kwargs['{0}_{1}'.format('is', 'active')] = True

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Soft delete
        instance.is_delete = True
        instance.save()
        # Or hard delete
        # instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
