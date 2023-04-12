from django.urls import path
from .views import RetriveArticles, ArticleDetail, FeaturedArticles, PopularArticles,CreateArticle,UpdateArticle,DeleteArticle

urlpatterns = [
    path('create-article/', CreateArticle, name = 'create_articles'),
    path('update-article/<int:article_id>/', UpdateArticle, name = 'update_articles'),
    path('delete-article/<int:article_id>/', DeleteArticle, name = 'delete_articles'),
    path('articles/', RetriveArticles, name = 'get_articles'),
    path('articles/<str:slug>/', ArticleDetail, name = 'article_details'),
    path('featured_articles/', FeaturedArticles, name = 'featured_articles'),
    path('popular_articles/', PopularArticles, name = 'popular_articles')
]
