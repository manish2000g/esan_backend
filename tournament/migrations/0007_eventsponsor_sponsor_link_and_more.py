# Generated by Django 4.2 on 2023-06-03 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_remove_tournamentsponsor_sponsor_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsponsor',
            name='sponsor_link',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='tournamentsponsor',
            name='sponsor_link',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]