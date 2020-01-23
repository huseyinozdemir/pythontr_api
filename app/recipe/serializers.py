from rest_framework import serializers

from core.models import Category, Article


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'parent_category', 'name', 'short_name',
                  'full_category_name')
        reod_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'categories', 'title', 'title_h1',
                  'description', 'content', 'read_count', 'user',
                  'is_active', 'is_approval', 'approval_user', 'is_delete',)
        reod_only_fields = ('id', 'is_delete', 'is_active', 'read_count',)
