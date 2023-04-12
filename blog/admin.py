from django.contrib import admin
from . models import ArticleCategory, Article, Tag
# Register your models here.

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Tag)