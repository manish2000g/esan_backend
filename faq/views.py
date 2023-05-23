from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from faq.models import FAQ
from faq.serializers import FAQSerializer

@api_view(["POST"])
def CreateFAQ(request):
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

@api_view(["PUT"])
def UpdateFAQ(request):
    idd = request.GET.get("id")
    faq = FAQ.objects.get(id=idd )
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')
    value =request.POST.get('value')

    faq.heading = heading
    faq.detail = detail
    faq.value = value

    faq.save()
    return Response({"FAQ Updated Successfully"})


@api_view(["GET"])
def FAQList(request):
    faq = FAQ.objects.all()
    serializers = FAQSerializer(faq, many = True)
    return Response({
        "FAQs": serializers.data
    })


@api_view(["DELETE"])
def DeleteFAQ(request):
    idd = request.GET.get("id")
    faq = FAQ.objects.get(id=idd )
    faq.delete()
    return Response({"FAQ Deleted Successfully"})


