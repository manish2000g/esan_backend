# Generated by Django 4.2 on 2023-05-25 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_team_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_type',
            field=models.CharField(choices=[('Duo', 'Duo'), ('Squad', 'Squad')], default='Squad', max_length=500),
        ),
    ]
