# Generated by Django 3.0.6 on 2020-07-04 16:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelines', '0016_delete_userextend'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatepost',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, related_name='bookmarked', to=settings.AUTH_USER_MODEL),
        ),
    ]
