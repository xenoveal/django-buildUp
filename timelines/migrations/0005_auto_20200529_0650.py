# Generated by Django 3.0.6 on 2020-05-29 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timelines', '0004_auto_20200529_0644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookfor',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timelines.UserExtend'),
        ),
    ]
