from rest_framework import serializers

from core.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'title_h1', 'description',
                  'image', 'read_count', 'image_url', 'slug',
                  'user', 'username', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'slug', 'read_count',
                            'created_at', 'updated_at')
