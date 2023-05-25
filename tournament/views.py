from tournament.serializers import EventSerializer, TeamSerializer
from .models import Event,Team,Game
from account.models import UserProfile,Organization,Organizer,BlogWriter
from account.serializers import UserProfileSerializer
from .serializers import GameSerializer,GameSmallSerializer
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_team_initials(request):
    user = request.user
    organization = Organization.objects.get(user=user)
    players = organization.players.all()
    teams = Team.objects.filter(organization=organization)
    free_players = players.exclude(id__in=teams.values('players'))
    free_players_ser = UserProfileSerializer(free_players,many=True)
    gamess = Game.objects.all()
    gamess_serializer = GameSmallSerializer(gamess,many=True)
    return Response({"free_players":free_players_ser.data,"games":gamess_serializer.data},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    user = request.user
    if user.role == "Organization":
        players = request.POST.getlist("players")
        manager = request.POST.get("manager")
        team_name = request.POST.get("team_name")
        team_image = request.POST.get("team_image")
        game_id = request.POST.get("game_id")
        team_type = request.POST.get("team_type", "Squad")  # Default value set to "Squad" if not provided

        organization = Organization.objects.get(user=user)
        game = Game.objects.get(id=game_id)
        manager_profile = UserProfile.objects.get(id=manager)

        team = Team.objects.create(
            team_name=team_name,
            team_image=team_image,
            game=game,
            organization=organization,
            manager=manager_profile,
            team_type=team_type
        )

        players_to_add = UserProfile.objects.filter(id__in=players)
        team.players.set(players_to_add)

        return Response({"success": "Team created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Unauthorized for creating a team"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_team(request):
    user = request.user
    team_id = request.GET.get("id")

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if user.role == "Organization":
        players = request.POST.getlist("players")
        manager = request.POST.get("manager")
        team_name = request.POST.get("team_name")
        team_image = request.POST.get("team_image")
        game_id = request.POST.get("game_id")
        team_type = request.POST.get("team_type", team.team_type)  # Preserve existing value if not provided

        game = Game.objects.get(id=game_id)
        manager_profile = UserProfile.objects.get(id=manager)

        team.players.clear()
        players_to_add = UserProfile.objects.filter(id__in=players)
        team.players.set(players_to_add)

        team.team_name = team_name
        team.team_image = team_image
        team.manager = manager_profile
        team.game = game
        team.team_type = team_type
        team.save()

        return Response({"success": "Team updated"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to update the team"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_team(request):
    user = request.user
    team_id = request.POST.get("id")

    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return Response({"error": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if user.role != "Organization":
        return Response({"error": "Unauthorized to delete the team"}, status=status.HTTP_401_UNAUTHORIZED)

    team.delete()

    return Response({"success": "Team deleted"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_team(request):
    user = request.user
    organization = Organization.objects.get(user=user)
    myteams = Team.objects.filter(organization=organization)
    gamess = Game.objects.all()
    gamess_serializer = GameSmallSerializer(gamess,many=True)
    myteams_serializer = TeamSerializer(myteams,many=True)
    return Response({"teams":myteams_serializer.data,"games":gamess_serializer.data},status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_team(request):
    id = request.GET.get("id")
    team = Team.objects.get(id=id)
    serializer = TeamSerializer(team)
    return Response(serializer.data, status=status.HTTP_200_OK)


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

