from django.contrib import admin
from . models import ArticleCategory, Article, Tag
# Register your models here.

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Tag)

class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "is_featured",
        "is_popular",
        "is_verified",
        "is_published",
        "updated_at",
    )
    list_filter = ("updated_at", "is_popular", "is_verified","is_popular","is_featured")


admin.site.register(Article, ArticleAdmin)