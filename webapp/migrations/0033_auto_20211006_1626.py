# Generated by Django 3.2.7 on 2021-10-06 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0032_auto_20211003_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='movie',
            field=models.ManyToManyField(related_name='cast', related_query_name='has_cast', to='webapp.Movie'),
        ),
        migrations.AlterField(
            model_name='cast',
            name='tv',
            field=models.ManyToManyField(related_name='cast', related_query_name='has_cast', to='webapp.TV'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='movie',
            field=models.ManyToManyField(related_name='genre', related_query_name='has_genre', to='webapp.Movie'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='tv',
            field=models.ManyToManyField(related_name='genre', related_query_name='has_genre', to='webapp.TV'),
        ),
        migrations.AlterField(
            model_name='status',
            name='movie',
            field=models.ManyToManyField(related_name='status', related_query_name='has_status', to='webapp.Movie'),
        ),
        migrations.AlterField(
            model_name='status',
            name='tv',
            field=models.ManyToManyField(related_name='status', related_query_name='has_status', to='webapp.TV'),
        ),
    ]
