# Generated by Django 3.0.6 on 2020-05-30 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelines', '0012_auto_20200530_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='join',
            field=models.ManyToManyField(blank=True, related_name='joined', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privatepost',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Join',
        ),
    ]
