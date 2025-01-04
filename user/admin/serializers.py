from django.contrib.auth import get_user_model
from rest_framework import serializers


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'name', 'surname', "image",
                  'is_active', 'is_staff', 'is_ban',
                  'is_delete', 'created_at', 'updated_at']
        read_only_fields = ['email', 'name', 'created_at', 'updated_at']


class AdminUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'name', 'surname', "image",
                  'about_me', 'is_active', 'is_staff', 'is_ban',
                  'is_delete', 'created_at', 'updated_at']
        read_only_fields = ['email', 'name', 'surname', 'about_me',
                            'created_at', 'last_login']


class AdminUserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['is_active', 'is_staff', 'is_ban', 'is_delete']
