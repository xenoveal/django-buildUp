# Generated by Django 3.0.6 on 2020-07-15 12:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelines', '0027_content_contentimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='bookmarked',
            field=models.ManyToManyField(blank=True, related_name='info_bookmarked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='content',
            name='contentImage',
            field=models.ImageField(blank=True, upload_to='galery'),
        ),
    ]