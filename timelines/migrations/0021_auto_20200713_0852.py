# Generated by Django 3.0.6 on 2020-07-13 08:52

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelines', '0020_collaborationpost_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborationpost',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, related_name='colabs_bookmarked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collaborationpost',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
