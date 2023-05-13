from rest_framework import serializers
from .models import Testimonial
from account.serializers import UserProfileDetailSerializer

class TestimonialSerializer(serializers.ModelSerializer):
    user = UserProfileDetailSerializer(read_only=True)
    class Meta:
        model = Testimonial
        fields = '__all__'
