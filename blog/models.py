from django.db import models
from ckeditor.fields import RichTextField
from account.models import BlogWriter
    
class ArticleCategory(models.Model):
    c_name = models.CharField(max_length=50, help_text='Artcile Category Name')
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.c_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name

class Article(models.Model):
    slug = models.SlugField(unique=True)
    thumbnail_image = models.ImageField(upload_to='static/images')
    thumbnail_image_alt_description = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    article_content = RichTextField(max_length=500) 
    c_name = models.ManyToManyField(ArticleCategory, help_text='Article Category',related_name="categories")
    author = models.ForeignKey(BlogWriter,on_delete=models.DO_NOTHING,related_name="author")
    tags = models.ManyToManyField(Tag,related_name="tags")
    time_to_read = models.PositiveSmallIntegerField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField(max_length=400)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.article}' 