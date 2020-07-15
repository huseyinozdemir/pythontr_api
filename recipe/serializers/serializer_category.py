from rest_framework import serializers

from core.models import Category


class CategoryReleatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'parent_category', 'name', 'title', 'title_h1',
            'description', 'content', 'slug', 'short_name',
            'full_category_name', 'create_at', 'updated_at',
        )


class CategorySerializer(serializers.ModelSerializer):
    categories = CategoryReleatedSerializer(
        many=True, required=False,
        read_only=True,
        source='category_set'
    )

    class Meta:
        model = Category
        fields = ('id', 'parent_category', 'name', 'title', 'title_h1',
                  'description', 'content', 'slug', 'short_name',
                  'full_category_name', 'create_at', 'updated_at',
                  'categories',)
        reod_only_fields = ('id', 'create_at', 'updated_at', 'slug')
