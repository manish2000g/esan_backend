# Generated by Django 4.2 on 2023-04-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_blogwriter_email_remove_blogwriter_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
