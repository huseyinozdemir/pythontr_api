from rest_framework import serializers

from core.models import Article

from .serializer_comment import CommentSerializer


class ArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'categories', 'title', 'title_h1', 'description',
                  'content', 'image', 'read_count', 'image_url', 'slug',
                  'user', 'is_active', 'is_approval', 'approval_user',
                  'is_delete', 'comments', 'created_at', 'updated_at')
        read_only_fields = ('id', 'is_delete', 'is_active', 'slug',
                            'read_count', 'comments',
                            'created_at', 'updated_at')
