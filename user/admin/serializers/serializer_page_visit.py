from rest_framework import serializers
from core.models.model_page_visit import PageVisit


class PageVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageVisit
        fields = [
            'id', 'user', 'path', 'timestamp', 'ip_address',
            'user_agent', 'referrer', 'method', 'device_type',
            'language', 'session_id', 'extra_data'
        ]
        read_only_fields = ['timestamp']
