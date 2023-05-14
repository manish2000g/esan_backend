from tournament.serializers import EventSerializer
from .models import Event
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
def Create_Event(request):
    organizer_id = request.POST.get('organizer_id')
    event_name = request.POST.get('event_name')
    event_description = request.POST.get('event_description', '')
    event_start_date = request.POST.get('event_start_date')
    event_end_date = request.POST.get('event_end_date')

    event = Event.objects.create(
        organizer_id=organizer_id,
        event_name=event_name,
        event_description=event_description,
        event_start_date=event_start_date,
        event_end_date=event_end_date,
    )
    event.save()
    return Response({"success": "Successfully created Event"})


@api_view(['PUT'])
def Update_Event(request, pk):
    event = Event.objects.get( pk=pk)

    organizer_id = request.POST.getlist('organizer_id')
    event_name = request.POST.get('event_name')
    event_description = request.POST.get('event_description')
    event_start_date = request.POST.get('event_start_date')
    event_end_date = request.POST.get('event_end_date')

    event.organizer_id = organizer_id
    event.event_name = event_name
    event.event_description = event_description
    event.event_start_date = event_start_date
    event.event_end_date = event_end_date

    event.save()
    return Response({"success": "Successfully updated Event"})

@api_view(["GET"])
def EventList(request):
    event = Event.objects.all()
    serializers = EventSerializer(event, many = True)
    return Response({
        "Event": serializers.data
    })   

@api_view(["DELETE"])
def Delete_Event(request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})