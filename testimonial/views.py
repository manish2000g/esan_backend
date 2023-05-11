
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Testimonial
from .serializers import TestimonialSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_testimonial(request):
    serializer = TestimonialSerializer(data=request.data)
    if serializer.is_valid():
        testimonial = serializer.save(user=request.user)
        return Response({"testimonial_id": testimonial.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_testimonials(request):
    testimonials = Testimonial.objects.all()
    serializer = TestimonialSerializer(testimonials, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_testimonial(request, pk):
    testimonial = Testimonial.objects.get(pk=pk)
    serializer = TestimonialSerializer(testimonial)
    return Response(serializer.data)

@api_view(['PUT'])
def edit_testimonial(request, pk):
    testimonial = Testimonial.objects.get(pk=pk)
    serializer = TestimonialSerializer(testimonial, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_testimonial(request, pk):
    testimonial = Testimonial.objects.get(pk=pk)
    testimonial.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
