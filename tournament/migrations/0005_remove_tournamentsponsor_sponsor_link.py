# Generated by Django 4.2 on 2023-06-03 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0004_alter_tournament_tournament_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentsponsor',
            name='sponsor_link',
        ),
    ]
