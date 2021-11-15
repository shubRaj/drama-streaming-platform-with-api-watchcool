# Generated by Django 3.2.8 on 2021-11-04 21:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='updated_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='season',
            name='updated_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]