# Generated by Django 3.2.8 on 2021-11-21 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_episode_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ('-episode_number', '-added_on')},
        ),
    ]
