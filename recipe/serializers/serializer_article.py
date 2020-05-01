from rest_framework import serializers

from core.models import Article

from .serializer_comment import CommentSerializer


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'categories', 'title', 'title_h1',
                  'description', 'content', 'read_count', 'user',
                  'is_active', 'is_approval', 'approval_user', 'is_delete',
                  'comments',)
        reod_only_fields = ('id', 'is_delete', 'is_active', 'read_count',
                            'comments',)
