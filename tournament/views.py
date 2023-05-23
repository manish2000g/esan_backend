from tournament.serializers import EventSerializer
from .models import Event,Team,Game
from account.models import UserProfile,Organization,Organizer,BlogWriter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTeam(request):
    user = request.user
    if user.role == "Organization":
        players = request.POST.getlist("players")
        manager = request.POST.get("manager")
        team_name = request.POST.get("team_name")
        team_image = request.POST.get("team_name")
        game_id = request.POST.get("game_id")
        organization = Organization.objects.get(user=user)
        gamee = Game.objects.get(id=game_id)
        teamm = Team.objects.create(team_name=team_name,team_image=team_image,game=gamee,organization=organization,manager=manager)
        for player in players :
            pll = UserProfile.objects.get(id=player)
            teamm.players.add(pll)
        teamm.save()
        return Response({"success":"Team Created"},status=status.HTTP_200_OK)
    else:
        return Response({"error":"Unauthourized for creating team"},status=status.HTTP_401_UNAUTHORIZED)