# Generated by Django 4.2 on 2023-05-26 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_tournament_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(max_length=700, unique=True),
        ),
    ]