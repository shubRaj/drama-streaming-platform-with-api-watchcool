# Generated by Django 3.2.8 on 2021-11-13 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20211109_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tv',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
