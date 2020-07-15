# Generated by Django 3.0.6 on 2020-07-15 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelines', '0025_content_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='guidebook',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='collaborationpost',
            name='paragraph',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='commentprivatepost',
            name='paragraph',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='content',
            name='paragraph',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='privatepost',
            name='paragraph',
            field=models.TextField(max_length=300),
        ),
    ]
