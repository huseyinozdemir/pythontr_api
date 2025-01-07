import re
import json

from datetime import timedelta
from user_agents import parse

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from django.utils import timezone
from django.db.models import F, Q
from django.db.models import Count, Avg
from django.db.models.functions import ExtractHour
from django.http import JsonResponse

from core.models.model_page_visit import PageVisit
from core.models.model_article import Article

from user.admin import serializers


class PageVisitViewSet(viewsets.ModelViewSet):
    queryset = PageVisit.objects.all()
    serializer_class = serializers.PageVisitSerializer

    def get_permissions(self):
        if self.action in ['track_page_visit', 'visitor_statistics',
                           'content_performance', 'referrer_analysis']:
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
            'phantom', 'headless', 'selenium',
            'mediapartners-google', 'adsbot-google'
        ]
        return any(bot in ua_string.lower() for bot in common_bot_strings) or \
            user_agent.is_bot

    def _get_request_data(self, request):
        """Extract and process request data"""

        ip_address = (
            request.META.get('HTTP_X_FORWARDED_FOR', '') or
            request.META.get('HTTP_X_REAL_IP', '') or
            request.META.get('REMOTE_ADDR', '')
        ).split(',')[0].strip()

        if ip_address in ('127.0.0.1', '::1', 'localhost'):
            return None

        try:
            body_data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            body_data = {}

        path = body_data.get('path', request.path)
        content_id = None

        if match := re.search(r'(.*?)-(\d+)$', path):
            content_id = match.group(2)
            Article.objects.filter(pk=content_id).update(
                read_count=F('read_count') + 1
            )

        return {
            'path': path,
            'content_id': content_id,
            'referrer': body_data.get('referrer',
                                      request.META.get('HTTP_REFERER')),
            'ip_address': ip_address,
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

        content_owner = None
        if data['content_id']:
            try:
                content = Article.objects.get(id=data['content_id'])
                content_owner = content.user
            except Article.DoesNotExist:
                pass

        page_visit = PageVisit(
            # user=request.user if request.user.is_authenticated else None,
            user=content_owner,
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

    def _get_date_range(self, period):
        """Calculate date range for a given period"""
        now = timezone.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:  # all time
            return None, None
        return start_date, now

    def _filter_queryset(self, queryset, request):
        """Filter queryset based on parameters"""
        period = request.query_params.get('period')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        user_id = request.user.id

        # Date filter
        if start_date and end_date:
            queryset = queryset.filter(
                timestamp__range=[start_date, end_date])
        elif period:
            start_date, end_date = self._get_date_range(period)
            if start_date and end_date:
                queryset = queryset.filter(
                    timestamp__range=[start_date, end_date])

        # User filter
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    @action(detail=False, methods=['GET'])
    def visitor_statistics(self, request):
        """Visitor statistics"""
        queryset = self._filter_queryset(PageVisit.objects.all(), request)

        stats = {
            'period_info': {
                'period': request.query_params.get('period', 'all'),
                'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
            },
            'total_visits': queryset.count(),
            'device_distribution': list(
                queryset.values('device_type').annotate(
                    count=Count('id'))),
            'browser_distribution': list(queryset.values('browser').annotate(
                count=Count('id')
            )),
            'os_distribution': list(queryset.values('os').annotate(
                count=Count('id')
            )),
            'most_visited_pages': list(queryset.values('path').annotate(
                visit_count=Count('id')
            ).order_by('-visit_count')[:10]),
            'traffic_by_hour': list(queryset.annotate(
                hour=ExtractHour('timestamp')
            ).values('hour').annotate(count=Count('id')).order_by('hour')),
        }
        return JsonResponse(stats)

    @action(detail=False, methods=['GET'])
    def content_performance(self, request):
        """Content performance metrics"""
        queryset = self._filter_queryset(
            PageVisit.objects.filter(content_id__isnull=False),
            request
        )

        performance = list(queryset.values(
            'content_id'
        ).annotate(
            total_visits=Count('id'),
            unique_visitors=Count('ip_address', distinct=True),
            avg_time_spent=Avg('time_spent'),
            device_breakdown=Count('device_type'),
        ).order_by('-total_visits'))

        return JsonResponse({
            'period_info': {
                'period': request.query_params.get('period', 'all'),
                'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
            },
            'performance': performance
        })

    @action(detail=False, methods=['GET'])
    def referrer_analysis(self, request):
        """Referrer analysis"""
        queryset = self._filter_queryset(
            PageVisit.objects.exclude(
                Q(referrer__isnull=True) | Q(referrer='')
            ),
            request
        )

        referrers = list(queryset.values('referrer').annotate(
            visit_count=Count('id'),
            unique_visitors=Count('ip_address', distinct=True)
        ).order_by('-visit_count'))

        return JsonResponse({
            'period_info': {
                'period': request.query_params.get('period', 'all'),
                'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
            },
            'referrers': referrers
        })
