from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Article

from recipe import serializers
from recipe.permissions import IsAuthenticatedAndOwner

from .baseview import BaseViewSet


class ArticleViewSet(BaseViewSet, mixins.CreateModelMixin):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes_by_action = {
        'list': [AllowAny], 'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticatedAndOwner],
    }

    def get_queryset(self):
        articles = self.request.query_params.get('search', None)
        me = self.request.query_params.get('me', None)
        queryset = self.queryset
        if articles:
            queryset = queryset.filter(title__icontains=articles,
                                       is_active=True,
                                       is_delete=False)
        if me:
            request = self.request
            if not request or not queryset:
                return None
            queryset = queryset.filter(user=request.user, is_delete=False)
        if self.action == 'list':
            newquery = queryset.filter(
                is_active=True,
                is_delete=False
            ).all().order_by('-id').distinct()
            queryset = newquery
        return queryset
