# Generated by Django 3.2.25 on 2024-12-14 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
