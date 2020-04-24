from rest_framework import serializers

from core.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'create_at', 'sender', 'user', 'subject', 'content',
                  'ip', 'is_read', 'is_delete',)
        reod_only_fields = ('id',)
