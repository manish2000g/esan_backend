# Generated by Django 4.2 on 2023-04-12 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='logo',
            field=models.ImageField(null=True, upload_to='media/static/images/organizer_logos/'),
        ),
    ]