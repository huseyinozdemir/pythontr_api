from rest_framework import serializers

from core.models import Category, Article, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'parent_category', 'name', 'short_name',
                  'full_category_name')
        reod_only_fields = ('id',)


class CommentReleatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'content',
            'email',
            'name',
            'object_id',
        )


class CommentSerializer(serializers.ModelSerializer):
    comments = CommentReleatedSerializer(many=True, required=False,
                                         read_only=True)

    class Meta:
        model = Comment
        fields = (
            'content',
            'email',
            'name',
            'object_id',
            'comments',
        )


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
