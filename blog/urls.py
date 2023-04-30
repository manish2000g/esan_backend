from django.urls import path
from .views import Article_Category_Detail, Create_Article_Category, Create_Tag, Delete_Tag, Get_Article_Category, Get_Tag, RetriveArticles, Article_Detail, FeaturedArticles, PopularArticles,CreateArticle, Update_Article_Category, Update_Tag,UpdateArticle,DeleteArticle

urlpatterns = [
    path('create-article_category/', Create_Article_Category, name = 'create_article_category'),
    path('update-article-category/<int:category_id>/', Update_Article_Category, name = 'update_article_category'),
    path('delete-article-category/<int:category_id>/', DeleteArticle, name = 'delete_articles'),
    path('article-category/', Get_Article_Category, name = 'get_article_category'),
    path('article-category/<str:slug>/', Article_Category_Detail, name = 'article_category_details'),
    path('create-article/', CreateArticle, name = 'create_articles'),
    path('update-article/<int:article_id>/', UpdateArticle, name = 'update_articles'),
    path('delete-article/<int:article_id>/', DeleteArticle, name = 'delete_articles'),
    path('articles/', RetriveArticles, name = 'get_articles'),
    path('create-tag/', Create_Tag, name = 'create_tag'),
    path('update-article/<int:tag_id>/', Update_Tag, name = 'update_tag'),
    path('delete-article/<int:tag_id>/', Delete_Tag, name = 'delete_tags'),
    path('tags/', Get_Tag, name = 'get_tags'),
    path('articles/<str:slug>/', Article_Detail, name = 'article_details'),
    path('featured_articles/', FeaturedArticles, name = 'featured_articles'),
    path('popular_articles/', PopularArticles, name = 'popular_articles')
]
