# Generated by Django 4.2 on 2023-05-07 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_blogwriter_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.CharField(default='Nepal', max_length=100),
        ),
    ]