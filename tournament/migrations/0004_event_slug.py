# Generated by Django 4.2 on 2023-05-26 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_rename_event_thumbnail_description_event_event_thumbnail_alt_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='sdv', max_length=700),
            preserve_default=False,
        ),
    ]