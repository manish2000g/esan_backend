# Generated by Django 4.2 on 2023-05-02 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_article_options_alter_article_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='active',
        ),
    ]