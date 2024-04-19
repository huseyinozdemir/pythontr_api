from rest_framework import serializers

from core.models import Slider


class SliderSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Slider
        fields = ('id', 'title', 'description', 'link',
                  'image', 'image_url', 'user', 'username', 'is_active',
                  'is_approval', 'approval_user', 'is_delete', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'is_delete', 'is_active', 'created_at',
                            'updated_at')
