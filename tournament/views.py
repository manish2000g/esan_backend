from .models import Event, EventFAQ, EventSponsor,Team,Game, Tournament, TournamentFAQ, TournamentSponsor
from account.models import Organizer, UserProfile,Organization
from account.serializers import UserProfileSerializer
from .serializers import EventFAQSerializer, EventSponsorSerializer,GameSmallSerializer, TournamentFAQSerializer, TournamentSerializer, TournamentSponsorSerializer, EventSerializer, TeamSerializer,EventSmallSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer":
            return Response({"error": "Only organizers can create events"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description', '')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')

        organizer = Organizer.objects.get(user=user)

        event = Event.objects.create(
            organizer=organizer,
            event_name=event_name,
            event_description=event_description,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
        )
        event.save()
        return Response({"success": "Successfully created Event"})
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event(request):
    try:
        pk = request.GET.get("id")
        event = Event.objects.get(id=pk)
        user = request.user

        # Check if the user is the organizer of the event
        if event.organizer.user != user:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')

        event.event_name = event_name
        event.event_description = event_description
        event.event_start_date = event_start_date
        event.event_end_date = event_end_date

        event.save()
        return Response({"success": "Successfully updated Event"})
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def event_list(request):
    user= request.user
    orgg = Organizer.objects.get(user=user)
    event = Event.objects.filter(organizer=orgg)
    serializers = EventSmallSerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   

@api_view(["GET"])
def all_event_list(request):
    event = Event.objects.all()
    serializers = EventSmallSerializer(event, many = True)
    return Response({
        "events": serializers.data
    })   


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request):
    pk = request.GET.get('id')
    event = Event.objects.get(id = pk)
    event_serializer = EventSerializer(event)
    faq = EventFAQ.objects.filter(event = event)
    faq_serializer = EventFAQSerializer(faq, many = True)
    sponsor = EventSponsor.objects.filter(event = event)
    sponsor_serializer = EventSponsorSerializer(sponsor, many = True)
    return Response({
        'event': event_serializer.data,
        'faq': faq_serializer.data,
        'sponsor': sponsor_serializer.data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_event(request):
    idd = request.GET.get("id")
    event = Event.objects.get(id=idd)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_faq(request):
    event_id = request.POST.get('id')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.create(
        event=event,
        value=value,
        heading=heading,
        detail=detail
    )
    faq.save()

    return Response({"success": "Event FAQ created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_faq(request):
    faq_id = request.POST.get('id')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        faq = EventFAQ.objects.get(id=faq_id)
    except EventFAQ.DoesNotExist:
        return Response({"error": "Event FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq.value = value
    faq.heading = heading
    faq.detail = detail
    faq.save()

    return Response({"success": "Event FAQ updated successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_faq_list(request):
    event_faq = EventFAQ.objects.all()
    serializers = EventFAQSerializer(event_faq, many = True)
    return Response({
        "event_faqs": serializers.data
    })  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_faq(request):
    pk = request.GET.get('id')
    faq = EventFAQ.objects.get(id = pk)
    serializer = EventFAQSerializer(faq)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_faq(request):
    pk = request.GET.get("id")
    event_faq = EventFAQ.objects.get(id=pk)
    event_faq.delete()
    return Response({"success": "EventFAQ deleted successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_sponsor_list(request):
    event_faq = EventSponsor.objects.all()
    serializers = EventSponsorSerializer(event_faq, many = True)
    return Response({
        "event_sponsors": serializers.data
    }) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_sponsor(request):
    pk = request.GET.get('id')
    sponsor = EventSponsor.objects.get(id = pk)
    serializer = EventSponsorSerializer(sponsor)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_sponsor(request):
    event_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_banner = request.FILES.get('sponsor_banner')

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor = EventSponsor.objects.create(
        event=event,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_banner=sponsor_banner
    )
    sponsor.save()

    return Response({"success": "Event Sponsor created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_sponsor(request):
    sponsor_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_banner = request.POST.get('sponsor_banner')

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.sponsor_name = sponsor_name
    sponsor.sponsorship_category = sponsorship_category
    sponsor.sponsor_banner = sponsor_banner

    sponsor.save()

    return Response({"success": "Event Sponsor updated successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_sponsor(request):
    event_sponsor_id = request.GET.get("id")
    event_sponsor = EventSponsor.objects.get(id=event_sponsor_id)
    event_sponsor.delete()
    return Response({"success": "EventSponsor deleted successfully"})
    


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
        team_image = request.FILES.get("team_image")
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
        manager = request.POST.get("manager",team.manager.id)
        team_name = request.POST.get("team_name",team.team_name)
        team_image = request.FILES.get("team_image",None)
        game_id = request.POST.get("game_id",team.game.id)
        team_type = request.POST.get("team_type", team.team_type)  # Preserve existing value if not provided

        game = Game.objects.get(id=game_id)
        manager_profile = UserProfile.objects.get(id=manager)

        team.players.clear()
        players_to_add = UserProfile.objects.filter(id__in=players)
        team.players.set(players_to_add)

        print(team_image)
        team.team_name = team_name
        if team_image:
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
    return Response({"team_detail":serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team(request):
    user = request.user
    idd = request.GET.get("id")
    team = Team.objects.get(id=idd)

    if user.role == "Organization":
        team.delete()
        return Response({"success": "Team Deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Unauthorized to delete the team"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournaments_list(request):
    tournaments = Tournament.objects.all()
    serializers = EventSerializer(tournaments, many = True)
    return Response({
        "tournaments": serializers.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer":
            return Response({"error": "Only organizers can create tournaments"}, status=status.HTTP_403_FORBIDDEN)

        tournament_name = request.data.get('tournament_name', '')
        tournament_logo = request.data.get('tournament_logo', None)
        tournament_mode = request.data.get('tournament_mode', 'Online')
        tournament_participants = request.data.get('tournament_participants', 'Players')
        is_free = bool(request.data.get('is_free', False))
        tournament_fee = request.data.get('tournament_fee', None)
        maximum_no_of_participants = request.data.get('maximum_no_of_participants')
        game_id = request.data.get('id')
        tournament_description = request.data.get('tournament_description', '')
        tournament_rules = request.data.get('tournament_rules', '')
        tournament_prize_pool = request.data.get('tournament_prize_pool', '')
        registration_opening_date = request.data.get('registration_opening_date')
        registration_closing_date = request.data.get('registration_closing_date')
        tournament_start_date = request.data.get('tournament_start_date')
        tournament_end_date = request.data.get('tournament_end_date')
        is_published = bool(request.data.get('is_published', False))
        is_registration_enabled = bool(request.data.get('is_registration_enabled', False))
        accept_registration_automatic = bool(request.data.get('accept_registration_automatic', False))
        contact_email = request.data.get('contact_email', '')
        discord_link = request.data.get('discord_link', '')

        game = Game.objects.get(id=game_id)
        organizer = Organizer.objects.get(user=user)

        tournament = Tournament(
            organizer=organizer,
            tournament_name=tournament_name,
            tournament_logo=tournament_logo,
            tournament_mode=tournament_mode,
            tournament_participants=tournament_participants,
            is_free=is_free,
            tournament_fee=tournament_fee,
            maximum_no_of_participants=maximum_no_of_participants,
            game=game,
            tournament_description=tournament_description,
            tournament_rules=tournament_rules,
            tournament_prize_pool=tournament_prize_pool,
            registration_opening_date=registration_opening_date,
            registration_closing_date=registration_closing_date,
            tournament_start_date=tournament_start_date,
            tournament_end_date=tournament_end_date,
            is_published=is_published,
            is_registration_enabled=is_registration_enabled,
            accept_registration_automatic=accept_registration_automatic,
            contact_email=contact_email,
            discord_link=discord_link,
        )
        tournament.save()
        return Response({"success": "Tournament created successfully"})
    except Game.DoesNotExist:
        return Response({"error": "Invalid game ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Organizer.DoesNotExist:
        return Response({"error": "Organizer not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_detail(request):
    pk = request.GET.get('id')
    tournament = Tournament.objects.get(id = pk)
    tournament_serializer = TournamentSerializer(tournament)
    faq = TournamentFAQ.objects.filter(tournament = tournament)
    faq_serializer = TournamentFAQSerializer(faq, many = True)
    sponsor = TournamentSponsor.objects.filter(tournament = tournament)
    sponsor_serializer = TournamentSponsorSerializer(sponsor, many = True)
    return Response({
        'tournament': tournament_serializer.data,
        'faq': faq_serializer.data,
        'sponsor': sponsor_serializer.data
    })
   

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tournament(request):
    pk = request.GET.get("id")
    tournament = Tournament.objects.get(id=pk)
    user = request.user
    tournament_name = request.POST.get('tournament_name')
    tournament_logo = request.POST.get('tournament_logo')
    tournament_mode = request.POST.get('tournament_mode')
    tournament_participants = request.POST.get('tournament_participants')
    is_free = request.POST.get('is_free')
    tournament_fee = request.POST.get('tournament_fee')
    maximum_no_of_participants = request.POST.get('maximum_no_of_participants')
    game_id = request.POST.get('id')
    tournament_description = request.POST.get('tournament_description')
    tournament_rules = request.POST.get('tournament_rules')
    tournament_prize_pool = request.POST.get('tournament_prize_pool')
    registration_opening_date = request.POST.get('registration_opening_date')
    registration_closing_date = request.POST.get('registration_closing_date')
    tournament_start_date = request.POST.get('tournament_start_date')
    tournament_end_date = request.POST.get('tournament_end_date')
    is_published = request.POST.get('is_published')
    is_registration_enabled = request.POST.get('is_registration_enabled')
    accept_registration_automatic = request.POST.get('accept_registration_automatic')
    contact_email = request.POST.get('contact_email')
    discord_link = request.POST.get('discord_link')

    game = Game.objects.get(id = game_id)

    if tournament.organizer.user != user:
        return Response({"error": "You are not authorized to update this Tournament"}, status=status.HTTP_403_FORBIDDEN)

    tournament.tournament_name = tournament_name
    tournament.tournament_logo = tournament_logo
    tournament.tournament_mode = tournament_mode
    tournament.tournament_participants = tournament_participants
    tournament.is_free = is_free
    tournament.tournament_fee = tournament_fee
    tournament.maximum_no_of_participants = maximum_no_of_participants
    tournament.game = game
    tournament.tournament_description = tournament_description
    tournament.tournament_rules = tournament_rules
    tournament.tournament_prize_pool = tournament_prize_pool
    tournament.registration_opening_date = registration_opening_date
    tournament.registration_closing_date = registration_closing_date
    tournament.tournament_start_date = tournament_start_date
    tournament.tournament_end_date = tournament_end_date
    tournament.is_published = is_published
    tournament.is_registration_enabled = is_registration_enabled
    tournament.accept_registration_automatic = accept_registration_automatic
    tournament.contact_email = contact_email
    tournament.discord_link = discord_link

    tournament.save()
    return Response({"success": "Tournament updated successfully"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament(request):
    pk = request.GET.get("id")
    tournament = Tournament.objects.get(id=pk)
    tournament.delete()
    return Response({"success": "Tournament deleted successfully"})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_sponsor(request):
    tournament_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_logo = request.FILES.get('sponsor_logo')
    sponsor_link = request.POST.get('sponsor_link')
    sponsor_banner = request.FILES.get('sponsor_banner')

    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_sponsor = TournamentSponsor.objects.create(
        tournament=tournament,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_logo=sponsor_logo,
        sponsor_link=sponsor_link,
        sponsor_banner=sponsor_banner
    )
    tournament_sponsor.save()
    return Response({"success": "TournamentSponsor created successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_sponsor_list(request):
    tournament_sponsors = TournamentSponsor.objects.all()
    serializer = TournamentSponsorSerializer(tournament_sponsors, many=True)
    return Response({"tournament_sponsors": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_sponsor(request):
    pk = request.GET.get('id')
    sponsor = TournamentSponsor.objects.get(id = pk)
    serializer = TournamentSponsorSerializer(sponsor)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tournament_sponsor(request):
    sponsor_id = request.POST.get('id')
    sponsor_name = request.data.get('sponsor_name')
    sponsorship_category = request.data.get('sponsorship_category')
    sponsor_logo = request.data.get('sponsor_logo')
    sponsor_link = request.data.get('sponsor_link')
    sponsor_banner = request.data.get('sponsor_banner')

    try:
        tournament_sponsor = TournamentSponsor.objects.get(id=sponsor_id)
    except TournamentSponsor.DoesNotExist:
        return Response({"error": "Tournament Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_sponsor.sponsor_name = sponsor_name
    tournament_sponsor.sponsorship_category = sponsorship_category
    tournament_sponsor.sponsor_logo = sponsor_logo
    tournament_sponsor.sponsor_link = sponsor_link
    tournament_sponsor.sponsor_banner = sponsor_banner

    tournament_sponsor.save()
    return Response({"success": "TournamentSponsor updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_sponsor(request):
    sponsor_id = request.GET.get("id")
    tournament_sponsor = TournamentSponsor.objects.get(id=sponsor_id)
    tournament_sponsor.delete()
    return Response({"success": "TournamentSponsor deleted successfully"})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_faq(request):
    tournament_id = request.POST.get('id')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_faq = TournamentFAQ.objects.create(
        tournament = tournament,
        value=value,
        heading=heading,
        detail=detail
    )
    tournament_faq.save()
    return Response({"success": "TournamentFAQ created successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_faq_list(request):
    tournament_faqs = TournamentFAQ.objects.all()
    serializer = TournamentFAQSerializer(tournament_faqs, many=True)
    return Response({"tournament_faqs": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_faq(request):
    pk = request.GET.get('id')
    faq = TournamentFAQ.objects.get(id = pk)
    serializer = TournamentFAQSerializer(faq)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tournament_faq(request):
    faq_id = request.data.get('id')
    value = request.data.get('value')
    heading = request.data.get('heading')
    detail = request.data.get('detail')

    try:
        tournament_faq = TournamentFAQ.objects.get(id=faq_id)
    except TournamentFAQ.DoesNotExist:
        return Response({"error": "Tournament FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    tournament_faq.value = value
    tournament_faq.heading = heading
    tournament_faq.detail = detail

    tournament_faq.save()
    return Response({"success": "TournamentFAQ updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_faq(request):
    faq_id = request.GET.get("id")
    tournament_faq = TournamentFAQ.objects.get(id=faq_id)
    tournament_faq.delete()
    return Response({"success": "TournamentFAQ deleted successfully"})

