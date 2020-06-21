# Generated by Django 3.0.6 on 2020-06-03 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('user', '0002_auto_20200603_0603'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtend',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]
