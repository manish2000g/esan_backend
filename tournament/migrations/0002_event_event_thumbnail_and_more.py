# Generated by Django 4.2 on 2023-05-26 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_thumbnail',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='event',
            name='event_thumbnail_description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]