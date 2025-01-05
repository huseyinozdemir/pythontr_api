from django.utils import timezone
from datetime import timedelta


def get_time_based_stats(model):
    now = timezone.now()
    return {
        'today': model.objects.filter(created_at__date=now.date()).count(),
        'this_week': model.objects.filter(
            created_at__gte=now-timedelta(days=7)).count(),
        'this_month': model.objects.filter(
            created_at__month=now.month).count(),
    }
