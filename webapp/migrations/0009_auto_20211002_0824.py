# Generated by Django 3.2.7 on 2021-10-02 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20211002_0821'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='subtitle',
            table='movie_subtitle',
        ),
        migrations.AlterModelTable(
            name='watch',
            table='watch_movie',
        ),
    ]
