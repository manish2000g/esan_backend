from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

    
class ArticleCategory(models.Model):
    c_name = models.CharField(max_length=50, help_text='Artcile Category Name')
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.c_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name

class Articles(models.Model):
    slug = models.SlugField(unique=True)
    thumbnail_image = models.ImageField(upload_to='static/images')
    thumbnail_image_alt_description = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    article_content = RichTextField(max_length=500) 
    c_name = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, help_text='Article Category')
    author_name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    time_to_read = models.PositiveSmallIntegerField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(max_length=400)

    def __str__(self):
        return self.title