from django.shortcuts import render
from rest_framework.response import Response
from .seralizers import ArticleCategorySerializer, ArticleSerializer, CommentSerializer, TagSerializer
from .models import Article, ArticleCategory, Comment, Tag
from account.models import BlogWriter
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def Create_Article_Category(request):
    c_name = request.data.get('c_name')
    description = request.data.get('description')
    # Create a new ArticleCategory instance
    category = ArticleCategory(
        c_name=c_name,
    )
    category.save()

    return Response({'success': "Successfully created Article Category"})

@api_view(['PUT'])
def Update_Article_Category(request, category_id):
    category = get_object_or_404(ArticleCategory, id=category_id)
    c_name = request.data.get('c_name')
    category.c_name = c_name
    category.save()

    return Response({'success': "Successfully updated Article Category"})

@api_view(['DELETE'])
def Delete_Article_Category(request, category_id):
    category = get_object_or_404(ArticleCategory, id=category_id)
    category.delete()
    return Response({'success': "Successfully deleted Article Category"})

@api_view(['GET'])
def Get_Article_Category(request):
    category = ArticleCategory.objects.all()
    category_serializers = ArticleCategorySerializer(category, many=True)
    return Response(category_serializers.data)

@api_view(['GET'])
def Article_Category_Detail(request, slug):
    article_category = ArticleCategory.objects.get(slug=slug)
    serializer = ArticleCategorySerializer(article_category)
    return Response(serializer.data)

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
    is_published = request.POST.get('is_published')
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
        is_published =is_published, 
        meta_title=meta_title,
        meta_description=meta_description
    )
    article.save()

    # Add tags to the article
    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        article.tags.add(tag)

    return Response({'success': "Sucessfully Uploaded Article"})

@api_view(['POST'])
def create_comment(request):
    article_id = request.POST.get('article_id')
    name = request.POST.get('name')
    body = request.POST.get('body')
    parent_comment_id = request.POST.get('parent_comment_id')

    article = get_object_or_404(Article, id=article_id)

    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        comment = Comment(article=article, name=name, body=body, parent_comment=parent_comment)
    else:
        comment = Comment(article=article, name=name, body=body)

    comment.save()

    serializer = CommentSerializer(comment)

    return Response({'success': "Successfully Added Comment", 'comment': serializer.data})



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
    is_published = request.POST.get('is_published')
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
    article.is_published= is_published
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
def Article_Detail(request, slug):
    article = Article.objects.get(slug=slug)
    comments = Comment.objects.filter(article=article)
    serializer = ArticleSerializer(article)
    comments_serializer = CommentSerializer(comments, many=True)
    return Response({'article': serializer.data, 'comments': comments_serializer.data})

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

@api_view(['POST'])
def Create_Tag(request):
    tag_name = request.data.get('tag_name')
    # Create a new tag instance
    tag = Tag(
        tag_name=tag_name,
        
    )
    tag.save()

    return Response({'success': "Successfully created Tag"})

@api_view(['GET'])
def Get_Tag(request):
    tag = Tag.objects.all()
    serializers = TagSerializer(tag, many=True)
    return Response(serializers.data)

@api_view(['PUT'])
def Update_Tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag_name = request.data.get('tag_name')
    
    tag.tag_name = tag_name

    tag.save()
    return Response({'success': "Successfully updated Tag"})

def Delete_Tag(request, tag_id):
    # Retrieve the article to be deleted
    tag = get_object_or_404(Tag, id=tag_id)

    # Delete the article
    tag.delete()

    return Response({'success': "Sucessfully Deleted Tag"})