import re
import json

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from core.models.model_page_visit import PageVisit
from django.http import JsonResponse
from user_agents import parse

from user.admin import serializers


class PageVisitViewSet(viewsets.ModelViewSet):
    queryset = PageVisit.objects.all()
    serializer_class = serializers.PageVisitSerializer

    def get_permissions(self):
        if self.action in ['track_page_visit']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def _is_bot(self, ua_string: str, user_agent):
        """Check if the request is from a bot"""
        common_bot_strings = [
            'bot', 'crawler', 'spider', 'ping', 'lighthouse',
            'slurp', 'search', 'surveillance', 'monitoring',
            'analyzer', 'index', 'archive', 'scrape',
            'http', 'python-requests', 'curl', 'wget',
            'phantom', 'headless', 'selenium'
        ]
        return any(bot in ua_string.lower() for bot in common_bot_strings) or \
            user_agent.is_bot

    def _get_request_data(self, request):
        """Extract and process request data"""
        try:
            body_data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            body_data = {}

        path = body_data.get('path', request.path)
        content_id = None

        if match := re.search(r'(.*?)-(\d+)$', path):
            content_id = match.group(2)

        return {
            'path': path,
            'content_id': content_id,
            'referrer': body_data.get('referrer',
                                      request.META.get('HTTP_REFERER')),
            'ip_address': (
                request.META.get('HTTP_X_FORWARDED_FOR', '') or
                request.META.get('HTTP_X_REAL_IP', '') or
                request.META.get('REMOTE_ADDR', '')
            ),
            'language': request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')[:10],
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'ga_client_id': request.COOKIES.get('_ga'),
            'ga_session_id': request.COOKIES.get('_ga_369S5MD2X3'),
            'gads_id': request.COOKIES.get('__gads'),
            'gpi_uid': request.COOKIES.get('__gpi')
        }

    @action(detail=False, methods=['post'])
    def track_page_visit(self, request):
        data = self._get_request_data(request)
        user_agent = parse(data['user_agent'])

        if self._is_bot(data['user_agent'], user_agent):
            return JsonResponse(
                {'status': 'ignored', 'reason': 'bot_detected'})

        page_visit = PageVisit(
            user=request.user if request.user.is_authenticated else None,
            path=data['path'],
            content_id=data['content_id'],
            ip_address=data['ip_address'],
            user_agent=data['user_agent'],
            referrer=data['referrer'],
            method=request.method,
            language=data['language'],
            device_type=('mobile' if user_agent.is_mobile else
                         'tablet' if user_agent.is_tablet else 'desktop'),
            browser=user_agent.browser.family,
            os=user_agent.os.family,
            device_brand=user_agent.device.brand,
            device_model=user_agent.device.model,
            ga_client_id=data['ga_client_id'],
            ga_session_id=data['ga_session_id'],
            gads_id=data['gads_id'],
            gpi_uid=data['gpi_uid']
        )

        page_visit.save()
        return JsonResponse({'status': 'success'})
