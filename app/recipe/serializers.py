from rest_framework import serializers

from core.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'short_name',)
        reod_only_fields = ('id',)
