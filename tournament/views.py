from tournament.serializers import EventSerializer, TeamSerializer
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
def create_event(request):
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
def update_event(request):
    idd = request.GET.get("id")
    event = Event.objects.get( id=idd)
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
def event_list(request):
    event = Event.objects.all()
    serializers = EventSerializer(event, many = True)
    return Response({
        "Event": serializers.data
    })   

@api_view(["DELETE"])
def delete_event(request):
    idd = request.GET.get("id")
    event = Event.objects.get(id=idd)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_team(request, id):
    team = Team.objects.get(id=id)
    serializer = TeamSerializer(team)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_team(request, id):
    user = request.user
    team = Team.objects.get(id=id)

    if user.role == "Organization":
        team_name = request.POST.get("team_name")
        team_image = request.POST.get("team_image")
        manager = request.POST.get("manager")

        team.team_name = team_name 
        team.team_image = team_image 
        team.manager = manager 
        team.save()

        return Response({"success": "Team updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to update the team"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team(request, id):
    user = request.user
    team = Team.objects.get(id=id)

    if user.role == "Organization":
        team.delete()
        return Response({"success": "Team Deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to delete the team"}, status=status.HTTP_401_UNAUTHORIZED)

