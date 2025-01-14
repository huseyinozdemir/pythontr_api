# Generated by Django 4.2.17 on 2025-01-07 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_user_github'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('content_id', models.IntegerField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('referrer', models.URLField(blank=True, max_length=500, null=True)),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('PATCH', 'PATCH')], max_length=10)),
                ('device_type', models.CharField(choices=[('mobile', 'mobile'), ('tablet', 'tablet'), ('desktop', 'desktop')], default='unknown', max_length=50)),
                ('language', models.CharField(blank=True, default='en', max_length=10, null=True)),
                ('browser', models.CharField(blank=True, max_length=50, null=True)),
                ('os', models.CharField(blank=True, max_length=50, null=True)),
                ('device_brand', models.CharField(blank=True, max_length=50, null=True)),
                ('device_model', models.CharField(blank=True, max_length=50, null=True)),
                ('ga_client_id', models.CharField(blank=True, max_length=100, null=True)),
                ('ga_session_id', models.CharField(blank=True, max_length=100, null=True)),
                ('gads_id', models.CharField(blank=True, max_length=100, null=True)),
                ('gpi_uid', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['timestamp'], name='core_pagevi_timesta_df0357_idx'), models.Index(fields=['device_type'], name='core_pagevi_device__d70e25_idx'), models.Index(fields=['ip_address'], name='core_pagevi_ip_addr_037b80_idx')],
            },
        ),
    ]
