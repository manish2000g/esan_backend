from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from faq.models import FAQ
from faq.serializers import FAQSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_faq(request):
    user = request.get
    if user == 'Admin':
        heading = request.POST['heading']
        detail = request.POST['detail']
        value =request.POST['value']

        faq = FAQ.objects.create(
            heading = heading,
            detail = detail,
            value = value
        )
        faq.save()
        return Response({"FAQ created successfully"})
    else:
        return Response({"error":"Unauthourized for creating FAQ"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_faq(request):
    user = request.get
    idd = int(request.GET.get("id"))
    if user == 'Admin':
        faq = FAQ.objects.get(id=idd )
        heading = request.POST.get('heading')
        detail = request.POST.get('detail')
        value =request.POST.get('value')

        faq.heading = heading
        faq.detail = detail
        faq.value = value

        faq.save()
        return Response({"FAQ Updated Successfully"})
    else:
        return Response({"error":"Unauthourized for updating  FAQ"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def faq_list(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_faq(request):
    user = request.get
    idd = int(request.GET.get("id"))
    if user == 'Admin':
        faq = FAQ.objects.get(id=idd )
        faq.delete()
        return Response({"FAQ Deleted Successfully"})
    else:
        return Response({"error":"Unauthourized for deleting  FAQ"}, status=status.HTTP_401_UNAUTHORIZED)



