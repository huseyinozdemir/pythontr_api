from rest_framework import serializers

from core.models import Comment


class CommentReleatedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'email',
            'name',
            'ip',
            'user',
            'content_type',
            'object_id',
        )


class CommentSerializer(serializers.ModelSerializer):
    comments = CommentReleatedSerializer(many=True, required=False,
                                         read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'email',
            'name',
            'ip',
            'user',
            'content_type',
            'object_id',
            'comments',
        )
