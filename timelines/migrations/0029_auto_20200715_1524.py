# Generated by Django 3.0.6 on 2020-07-15 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timelines', '0028_auto_20200715_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='join',
        ),
        migrations.AddField(
            model_name='content',
            name='teams',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='for_joined', to='timelines.CollaborationPost'),
            preserve_default=False,
        ),
    ]
