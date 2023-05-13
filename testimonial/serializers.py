from rest_framework import serializers
from .models import Testimonial

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'description', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']
