from django.db import models
from django.contrib.auth import get_user_model


class PageVisit(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    path = models.CharField(max_length=255)
    content_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(max_length=500, null=True, blank=True)
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('PATCH', 'PATCH'),
    ]
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    DEVICE_TYPE_CHOICES = [
        ('mobile', 'mobile'),
        ('tablet', 'tablet'),
        ('desktop', 'desktop'),
    ]
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE_CHOICES,
                                   default='unknown')
    language = models.CharField(max_length=10, null=True, blank=True,
                                default='en')
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    device_brand = models.CharField(max_length=50, null=True, blank=True)
    device_model = models.CharField(max_length=50, null=True, blank=True)

    ga_client_id = models.CharField(max_length=100, null=True, blank=True)
    ga_session_id = models.CharField(max_length=100, null=True, blank=True)

    gads_id = models.CharField(max_length=100, null=True, blank=True)
    gpi_uid = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['device_type']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"{self.user} visited {self.path} at {self.timestamp}"
