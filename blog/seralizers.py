from rest_framework import serializers
from .models import  Article, ArticleCategory, Comment, Tag

class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    c_name = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Article
        fields = '__all__'
        ordering = ['-created_at']

class ArticleDetailSerializer(serializers.ModelSerializer):
    c_name = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Comment
        fields = '__all__' 