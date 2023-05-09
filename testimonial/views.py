
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
