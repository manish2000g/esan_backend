# Generated by Django 4.2 on 2023-05-02 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='category_name',
            new_name='categories',
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_popular',
        ),
    ]
