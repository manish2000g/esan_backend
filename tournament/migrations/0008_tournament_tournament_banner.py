# Generated by Django 4.2 on 2023-05-27 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_alter_event_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_banner',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]