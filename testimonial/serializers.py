from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'full_name', 'email', 'description', 'rating', 'is_published', 'created_at']
        read_only_fields = ['id', 'is_published', 'created_at']
