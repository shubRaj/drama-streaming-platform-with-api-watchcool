# Generated by Django 3.2.9 on 2022-01-17 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_alter_episode_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='source_url',
            field=models.CharField(blank=True, max_length=2083, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='source_url',
            field=models.CharField(blank=True, max_length=2083, null=True),
        ),
    ]
