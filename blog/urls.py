from django.urls import path
from .views import Article, Article_Detail, Featured_Articles, Popular_Articles

urlpatterns = [
    path('articles/', Article, name = 'articles'),
    path('articles/<str:slug>/', Article_Detail, name = 'article_details'),
    path('featured_articles/', Featured_Articles, name = 'featured_articles'),
    path('popular_articles/', Popular_Articles, name = 'popular_articles')
]
