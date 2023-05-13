from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from faq.models import FAQ
from faq.serializers import FAQSerializer
from rest_framework import status

# Create your views here.

@api_view(["POST"])
def Create_FAQ(request):
    serializer = FAQSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def Update_FAQ(request, pk):
    try:
        faq = FAQ.objects.get(pk=pk)
    except FAQ.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = FAQSerializer(faq, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def FAQList(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    })


@api_view(["DELETE"])
def delete_faq(request, pk):
    try:
        faq = FAQ.objects.get(pk=pk)
    except FAQ.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    faq.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


