# Generated by Django 4.2 on 2023-05-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_article_time_to_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='thumbnail_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]