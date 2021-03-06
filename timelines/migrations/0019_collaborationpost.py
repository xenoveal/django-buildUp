# Generated by Django 3.0.6 on 2020-07-13 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timelines', '0018_commentprivatepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollaborationPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('paragraph', models.CharField(max_length=300)),
                ('members', models.IntegerField()),
                ('location', models.CharField(max_length=50)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='needColabs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
