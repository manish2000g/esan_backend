# Generated by Django 4.2 on 2023-06-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0003_alter_tournament_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='tournament_fee',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
