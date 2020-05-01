from rest_framework import mixins
from rest_framework.permissions import AllowAny

from django.contrib.contenttypes.models import ContentType

from core.models import Article, Comment

from recipe import serializers

from .baseview import BaseViewSet
from .filter_param import RulesFilter, Search


class CommentViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny]}

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Article)
        search = self.request.query_params.get('search')
        queryset = []
        SearchKwargs = {
            '{0}__{1}'.format('name', 'icontains'): search,
        }

        rules = [
            Search(search, **SearchKwargs)
        ]

        kwargs = {
            '{0}_{1}'.format('is', 'active'): True,
            '{0}_{1}'.format('is', 'delete'): False,
            '{0}_{1}'.format('content', 'type'): content_type,
            '{0}__{1}'.format('object_id', 'in'): Article.objects.filter(
                is_active=True,
                is_delete=False
            ).all(),
        }

        rf = RulesFilter(rules)
        for item in rf.get_res():
            if item.is_check():
                kwargs.update(item.get_param())

        queryset = self.queryset.filter(
            **kwargs
        ).all().order_by('-id')

        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            # save anyone
            serializer.save()
        else:
            serializer.save(user=self.request.user)
