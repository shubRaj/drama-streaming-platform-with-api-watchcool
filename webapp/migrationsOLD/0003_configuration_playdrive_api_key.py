# Generated by Django 3.2.8 on 2021-10-27 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20211027_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='playdrive_api_key',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
