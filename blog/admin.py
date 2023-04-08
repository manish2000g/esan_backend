from django.contrib import admin
from . models import ArticleCategory, Articles, Tag
# Register your models here.

admin.site.register(ArticleCategory)
admin.site.register(Articles)
admin.site.register(Tag)