from rest_framework import mixins
from rest_framework.permissions import AllowAny

from django.contrib.contenttypes.models import ContentType

from core.models import Article, Comment

from recipe import serializers

from .baseview import BaseViewSet


class CommentViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes_by_action = {'create': [AllowAny],
                                    'list': [AllowAny]}

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Article)
        comments = self.request.query_params.get('search')
        queryset = self.queryset
        if comments:
            queryset = queryset.filter(content__icontains=comments)
        if self.action == 'list':
            queryset = queryset.filter(
                is_active=True,
                is_delete=False,
                # only active articles
                content_type=content_type,
                object_id__in=Article.objects.filter(
                    is_active=True,
                    is_delete=False
                ).all()
            ).all().order_by('-id')
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            # save anyone
            serializer.save()
        else:
            serializer.save(user=self.request.user)
