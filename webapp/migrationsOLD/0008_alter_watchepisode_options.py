# Generated by Django 3.2.8 on 2021-10-30 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20211029_1304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchepisode',
            options={'ordering': ('source',), 'verbose_name_plural': 'WatchEpisodes'},
        ),
    ]
