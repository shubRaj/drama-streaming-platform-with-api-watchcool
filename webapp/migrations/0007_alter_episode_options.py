# Generated by Django 3.2.8 on 2021-11-19 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20211113_1109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ('-added_on', '-episode_number')},
        ),
    ]
