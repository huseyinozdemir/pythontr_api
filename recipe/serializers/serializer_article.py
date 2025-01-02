from rest_framework import serializers
from django.utils.text import slugify

from core.models import Article

from .serializer_comment import CommentSerializer

import base64
from django.core.files.base import ContentFile


class ArticleSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'categories', 'title', 'title_h1', 'description',
                  'content', 'image', 'read_count', 'image_url', 'slug',
                  'user', 'username', 'is_active', 'is_approval',
                  'approval_user', 'is_delete', 'comments', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'is_delete', 'is_active', 'slug',
                            'read_count', 'comments',
                            'created_at', 'updated_at')

    def to_internal_value(self, data):
        if 'image' in data and data['image']:
            if isinstance(data['image'], str) and data[
                               'image'].startswith('data:image'):
                format, imgstr = data['image'].strip().split(';base64,')
                ext = format.split('/')[-1]

                if 'title' in data:
                    filename = slugify(data['title'])[:50]  # Uzunluğu sınırla
                else:
                    filename = 'temp'

                data = data.copy()
                data['image'] = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'{filename}.{ext}'
                )

        return super().to_internal_value(data)
