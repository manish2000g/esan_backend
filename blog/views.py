from django.shortcuts import render
from rest_framework.response import Response
from .seralizers import ArticleSerializer, TagSerializer
from .models import Article, Tag
from account.models import BlogWriter
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

def CreateArticle(request):
    # Extract the data sent from JavaScript
    slug = request.POST.get('slug')
    thumbnail_image = request.FILES.get('thumbnail_image')
    thumbnail_image_alt_description = request.POST.get('thumbnail_image_alt_description')
    title = request.POST.get('title')
    article_content = request.POST.get('article_content')
    author_id = request.POST.get('author_id')
    tags = request.POST.getlist('tags')
    time_to_read = request.POST.get('time_to_read')
    is_featured = request.POST.get('is_featured')
    is_popular = request.POST.get('is_popular')
    is_verified = request.POST.get('is_verified')
    meta_title = request.POST.get('meta_title')
    meta_description = request.POST.get('meta_description')

    # Retrieve the author instance
    author = get_object_or_404(BlogWriter, id=author_id)

    # Create a new article instance
    article = Article(
        slug=slug,
        thumbnail_image=thumbnail_image,
        thumbnail_image_alt_description=thumbnail_image_alt_description,
        title=title,
        article_content=article_content,
        author=author,
        time_to_read=time_to_read,
        is_featured=is_featured,
        is_popular=is_popular,
        is_verified=is_verified,
        meta_title=meta_title,
        meta_description=meta_description
    )
    article.save()

    # Add tags to the article
    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        article.tags.add(tag)

    return Response({'success': "Sucessfully Uploaded Article"})

def UpdateArticle(request, article_id):
    # Retrieve the article to be updated
    article = get_object_or_404(Article, id=article_id)

    # Extract the data sent from JavaScript
    slug = request.POST.get('slug')
    thumbnail_image = request.FILES.get('thumbnail_image')
    thumbnail_image_alt_description = request.POST.get('thumbnail_image_alt_description')
    title = request.POST.get('title')
    article_content = request.POST.get('article_content')
    author_id = request.POST.get('author_id')
    tags = request.POST.getlist('tags')
    time_to_read = request.POST.get('time_to_read')
    is_featured = request.POST.get('is_featured')
    is_popular = request.POST.get('is_popular')
    is_verified = request.POST.get('is_verified')
    meta_title = request.POST.get('meta_title')
    meta_description = request.POST.get('meta_description')

    # Retrieve the author instance
    author = get_object_or_404(BlogWriter, id=author_id)

    # Update the article fields
    article.slug = slug
    article.thumbnail_image = thumbnail_image
    article.thumbnail_image_alt_description = thumbnail_image_alt_description
    article.title = title
    article.article_content = article_content
    article.author = author
    article.time_to_read = time_to_read
    article.is_featured = is_featured
    article.is_popular = is_popular
    article.is_verified = is_verified
    article.meta_title = meta_title
    article.meta_description = meta_description
    article.tags.clear()  # Clear existing tags

    # Add tags to the article
    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        article.tags.add(tag)

    article.save()

    return Response({'success': "Sucessfully Updated Article"})

def DeleteArticle(request, article_id):
    # Retrieve the article to be deleted
    article = get_object_or_404(Article, id=article_id)

    # Delete the article
    article.delete()

    return Response({'success': "Sucessfully Deleted Article"})

@api_view(["GET"])
def RetriveArticles(request):
    featured_articles = Article.objects.filter(is_featured=True)
    featured_articles_serializers = ArticleSerializer(featured_articles, many = True)

    popoular_articles = Article.objects.filter(is_popular=True)
    popoular_artcles_serializers = ArticleSerializer(popoular_articles, many = True)

    tag = Tag.objects.all()
    tag_serializers = TagSerializer(tag, many = True)
    return Response({
        "featured_articles" : featured_articles_serializers.data,
        "popular_articles" : popoular_artcles_serializers.data,
        "tag" : tag_serializers.data
    })

@api_view(['GET'])
def ArticleDetail(request, slug):
    try:
        article_detail = Article.objects.get(slug=slug)
        article_detail_serializer = ArticleSerializer(article_detail)
        return Response(article_detail_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def FeaturedArticles(request):
    featured_articles = Article.objects.filter(is_featured=True).order_by('-id')[:10]
    serializer = [ArticleSerializer(article).data for article in featured_articles]
    return Response({'featured_articles': serializer})  


@api_view(["GET"])
def PopularArticles(request):
    popular_articles = Article.objects.filter(is_popular=True).order_by('-created_at')[:5]
    popular_articles_data = [ArticleSerializer(article).data for article in popular_articles]
    return Response(popular_articles_data)