# Generated by Django 3.2.8 on 2021-10-29 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20211027_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='playdrive_api_key',
        ),
    ]
