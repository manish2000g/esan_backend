import datetime
from .models import EliminationMode, Event, EventFAQ, EventNewsFeed, EventSponsor, Stage,Team,Game, TeamTournamentRegistration, Tournament, TournamentFAQ, TournamentSponsor, TournamentStreams
from account.models import Organizer, UserProfile,Organization
from account.serializers import UserProfileSerializer
from .serializers import EliminationModeSerializer, EventFAQSerializer, EventNewsFeedSerializer, EventSponsorSerializer,GameSerializer,GameSmallSerializer, StageSerializer, TeamTournamentRegistrationSerializer, TournamentFAQSerializer, TournamentSerializer, TournamentSponsorSerializer, EventSerializer, TeamSerializer,EventSmallSerializer, TournamentStreamsSerializer
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
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get("event_thumbnail")
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description', '')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')
        print(event_thumbnail)
        organizer = Organizer.objects.get(user=user)

        event = Event.objects.create(
            organizer=organizer,
            event_name=event_name,
            event_description=event_description,
            event_start_date=event_start_date,
            event_end_date=event_end_date,
            event_thumbnail=event_thumbnail,
            event_thumbnail_alt_description=event_thumbnail_alt_description,
            slug=slug
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
        idd = request.POST.get("id")
        event = Event.objects.get(id=idd)
        user = request.user

        # Check if the user is the organizer of the event
        if event.organizer.user != user:
            return Response({"error": "You are not authorized to update this event"}, status=status.HTTP_403_FORBIDDEN)

        event_name = request.POST.get('event_name')
        slug = request.POST.get('slug')
        event_thumbnail = request.FILES.get('event_thumbnail')
        event_thumbnail_alt_description = request.POST.get("event_thumbnail_alt_description")
        event_description = request.POST.get('event_description')
        event_start_date = request.POST.get('event_start_date')
        event_end_date = request.POST.get('event_end_date')

        print(event_thumbnail)

        event.event_name = event_name
        event.slug = slug
        if event_thumbnail:
            event.event_thumbnail = event_thumbnail
        event.event_thumbnail_alt_description = event_thumbnail_alt_description
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
def event_detail(request):
    slug = request.GET.get('slug')
    event = Event.objects.get(slug = slug)
    event_serializer = EventSerializer(event)
    faq = EventFAQ.objects.filter(event = event)
    faq_serializer = EventFAQSerializer(faq, many = True)
    sponsor = EventSponsor.objects.filter(event = event)
    sponsor_serializer = EventSponsorSerializer(sponsor, many = True)
    return Response({
        'event': event_serializer.data,
        'faqs': faq_serializer.data,
        'sponsors': sponsor_serializer.data
    })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_event(request):
    slug = request.GET.get("slug")
    event = Event.objects.get(slug=slug)
    event.delete()
    return Response({"success": "Event Deleted Successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_faq(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq = EventFAQ.objects.filter(event=event)
    faq_ser = EventFAQSerializer(faq,many=True)

    return Response({"FAQs": faq_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_sponsor(request):
    slug = request.GET.get('slug')
    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsors = EventSponsor.objects.filter(event=event)
    sponsors_ser = EventSponsorSerializer(sponsors,many=True)

    return Response({"sponsors": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_sponsor_detail(request):
    id = request.GET.get("id")
    sponsors = EventSponsor.objects.get(id=id)
    sponsors_ser = EventSponsorSerializer(sponsors)

    return Response({"sponsor_detail": sponsors_ser.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_faq(request):
    slug = request.POST.get('slug')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        event = Event.objects.get(slug=slug)
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
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

    try:
        faq = EventFAQ.objects.get(id=faq_id)
    except EventFAQ.DoesNotExist:
        return Response({"error": "Event FAQ does not exist"}, status=status.HTTP_404_NOT_FOUND)

    faq.heading = heading
    faq.detail = detail
    faq.save()

    return Response({"success": "Event FAQ updated successfully"})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_faq(request):
    id = request.GET.get("id")
    event_faq = EventFAQ.objects.get(id=id)
    event_faq.delete()
    return Response({"success": "EventFAQ deleted successfully"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_news_feed(request):
    slug = request.POST.get('slug')
    content = request.POST.get('content')
    user = request.user
    
    event = Event.objects.get(slug=slug)
    organizer = Organizer.objects.get(user=user)

    news_feed = EventNewsFeed.objects.create(
        event=event,
        content=content,
        user=organizer
    )
    news_feed.save()
    return Response({"success": "Event News Feed created successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_news_feed(request):
    slug = request.GET.get('slug')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feeds = EventNewsFeed.objects.filter(event=event)
    news_feeds_serializer = EventNewsFeedSerializer(news_feeds, many=True)

    return Response({"news_feeds": news_feeds_serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event_news_feed(request):
    news_feed_id = request.GET.get('id')
    content = request.POST.get('content')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.content = content
    news_feed.save()

    return Response({"success": "Event News Feed updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_news_feed(request):
    news_feed_id = request.GET.get('id')

    try:
        news_feed = EventNewsFeed.objects.get(id=news_feed_id)
    except EventNewsFeed.DoesNotExist:
        return Response({"error": "Event News Feed does not exist"}, status=status.HTTP_404_NOT_FOUND)

    news_feed.delete()

    return Response({"success": "Event News Feed deleted successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event_sponsor(request):
    slug = request.POST.get('slug')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    order = int(request.POST.get('order'))
    sponsor_banner = request.FILES.get('sponsor_banner')

    try:
        event = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor = EventSponsor.objects.create(
        event=event,
        sponsor_name=sponsor_name,
        sponsorship_category=sponsorship_category,
        sponsor_banner=sponsor_banner,
        order=order,
    )
    sponsor.save()

    return Response({"success": "Event Sponsor created successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_event_sponsor(request):
    sponsor_id = request.POST.get('id')
    sponsor_name = request.POST.get('sponsor_name')
    sponsorship_category = request.POST.get('sponsorship_category')
    sponsor_banner = request.FILES.get('sponsor_banner')
    order = int(request.POST.get('order'))

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.sponsor_name = sponsor_name
    sponsor.sponsorship_category = sponsorship_category
    sponsor.order = order

    if sponsor_banner:
        sponsor.sponsor_banner = sponsor_banner

    sponsor.save()

    return Response({"success": "Event Sponsor updated successfully"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event_sponsor(request):
    sponsor_id = request.GET.get('id')

    try:
        sponsor = EventSponsor.objects.get(id=sponsor_id)
    except EventSponsor.DoesNotExist:
        return Response({"error": "Event Sponsor does not exist"}, status=status.HTTP_404_NOT_FOUND)

    sponsor.delete()

    return Response({"success": "Event Sponsor deleted successfully"})



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
def tournaments_list(request):
    tournaments = Tournament.objects.all()
    serializers = TournamentSerializer(tournaments, many = True)
    return Response({
        "tournaments": serializers.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_tournaments_list(request):
    user = request.user
    eslug = request.GET.get("slug")
    event = Event.objects.get(slug=eslug)
    orgg = Organizer.objects.get(user=user)
    tournaments = Tournament.objects.filter(organizer=orgg,event=event)
    serializers = TournamentSerializer(tournaments, many = True)

    return Response({
        "tournaments": serializers.data
    },status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_elimination_mode(request):
    user = request.user
    if user.role == "Organizer":
        elimination_mode = request.POST.get('elimination_mode')

        mode = EliminationMode.objects.create(
            elimination_mode=elimination_mode
        )
        mode.save()
        return Response({"success": "Elimination mode created successfully"})
    else:
        return Response({"error": "Unauthorized to creating the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    mode = EliminationMode.objects.get(id=mode_id)
    serializer = EliminationModeSerializer(mode)
    return Response(serializer.data)

@api_view(['GET'])
def elimination_mode_list(request):
    elimination_mode = EliminationMode.objects.all()
    serializers = EliminationModeSerializer(elimination_mode, many = True)
    return Response({
        "elimination_modes": serializers.data
    })  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    user = request.user
    if user.role == "Organizer":
        elimination_mode = request.POST.get('elimination_mode')

        mode = EliminationMode.objects.get(id=mode_id)
        mode.elimination_mode = elimination_mode
        mode.save()
        return Response({"success": "Elimination mode updated successfully"})
    else:
        return Response({"error": "Unauthorized to updating the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_elimination_mode(request):
    mode_id = request.GET.get('mode_id')
    user = request.user
    if user.role == "Organizer":
        try:
            mode = EliminationMode.objects.get(id=mode_id)
            mode.delete()
            return Response({"success": "Elimination mode deleted successfully"})
        except EliminationMode.DoesNotExist:
            return Response({"error": "Elimination mode not found"})
    else:
        return Response({"error": "Unauthorized to deleting the elimiation mode"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_game(request):
    user = request.user
    if user.role == "Organizer":

        game_name = request.POST.get('game_name')
        game_image = request.POST.get('game_image')
        game_type = request.POST.get('game_type', 'Mobile')
        elimination_modes = request.POST.getlist('elimination_modes')

        game = Game.objects.create(
            game_name=game_name,
            game_image=game_image,
            game_type=game_type
        )

        for mode_id in elimination_modes:
            mode = EliminationMode.objects.get(id=mode_id)
            game.elimination_modes.add(mode)

        return Response({"success": "Game created successfully"})
    else:
        return Response({"error": "Unauthorized to create the game"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_game(request):
    elimination_mode_id = request.GET.get("id")
    elimination_mode = EliminationMode.objects.get(id=elimination_mode_id)
    game = Game.objects.filter(elimination_mode__id=elimination_mode)
    serializer = GameSerializer(game)
    return Response(serializer.data)


@api_view(['GET'])
def game_list(request):
    game = Game.objects.all()
    serializers = GameSerializer(game, many = True)
    return Response({
        "games": serializers.data
    })  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_game(request):
    game_id = request.GET.get('game_id')
    user = request.user
    if user.role == "Organizer":
        game_name = request.POST.get('game_name')
        game_image = request.POST.get('game_image')
        game_type = request.POST.get('game_type', 'Mobile')
        elimination_modes = request.POST.getlist('elimination_modes')

        try:
            game = Game.objects.get(id=game_id)
            game.game_name = game_name
            game.game_image = game_image
            game.game_type = game_type
            game.elimination_modes.clear()
            
            for mode_id in elimination_modes:
                mode = EliminationMode.objects.get(id=mode_id)
                game.elimination_modes.add(mode)

            game.save()
            return Response({"success": "Game updated successfully"})
        except Game.DoesNotExist:
            return Response({"error": "Game not found"})
    else:
        return Response({"error": "Unauthorized to update the game"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_game(request):
    game_id = request.GET.get('game_id')
    user = request.user
    if user.role == "Organizer":
        try:
            game = Game.objects.get(id=game_id)
            game.delete()
            return Response({"success": "Game deleted successfully"})
        except Game.DoesNotExist:
            return Response({"error": "Game not found"})
    else:
        return Response({"error": "Unauthorized to update the game"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament(request):
    try:
        user = request.user

        # Check if the user is an organizer
        if user.role != "Organizer":
            return Response({"error": "Only organizers can create tournaments"}, status=status.HTTP_403_FORBIDDEN)
        event_id = request.POST.get('event_id')
        tournament_name = request.POST.get('tournament_name', '')
        tournament_logo = request.FILES.get('tournament_logo', None)
        tournament_banner = request.FILES.get('tournament_banner', None)
        tournament_mode = request.POST.get('tournament_mode', 'Online')
        location = request.POST.get('location')
        tournament_participants = request.POST.get('tournament_participants', 'Players')
        is_free = bool(request.POST.get('is_free', False))
        tournament_fee = request.POST.get('tournament_fee', None)
        maximum_no_of_participants = request.POST.get('maximum_no_of_participants')
        game_id = request.POST.get('game_id')
        tournament_description = request.POST.get('tournament_description', '')
        tournament_short_description = request.POST.get('tournament_short_description', '')
        tournament_rules = request.POST.get('tournament_rules', '')
        tournament_prize_pool = request.POST.get('tournament_prize_pool', '')
        registration_opening_date = request.POST.get('registration_opening_date')
        registration_closing_date = request.POST.get('registration_closing_date')
        tournament_start_date = request.POST.get('tournament_start_date')
        tournament_end_date = request.POST.get('tournament_end_date')
        is_published = bool(request.POST.get('is_published', False))
        is_registration_enabled = bool(request.POST.get('is_registration_enabled', False))
        accept_registration_automatic = bool(request.POST.get('accept_registration_automatic', False))
        contact_email = request.POST.get('contact_email', '')
        discord_link = request.POST.get('discord_link', '')
        
        event = Event.objects.get(id=event_id)
        game = Game.objects.get(id=game_id)
        organizer = Organizer.objects.get(user=user)

        tournament = Tournament(
            organizer=organizer,
            event = event,
            tournament_name=tournament_name,
            tournament_logo=tournament_logo,
            tournament_banner=tournament_banner,
            tournament_mode=tournament_mode,
            location = location,
            tournament_participants=tournament_participants,
            is_free=is_free,
            tournament_fee=tournament_fee,
            maximum_no_of_participants=maximum_no_of_participants,
            game=game,
            tournament_description=tournament_description,
            tournament_short_description=tournament_short_description,
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
def tournament_detail(request, id):
    tournament = Tournament.objects.get(id = id)
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
    tournament_banner = request.FILES.get('tournament_banner', None)
    location = request.POST.get('location')
    tournament_mode = request.POST.get('tournament_mode')
    tournament_participants = request.POST.get('tournament_participants')
    is_free = request.POST.get('is_free')
    tournament_fee = request.POST.get('tournament_fee')
    maximum_no_of_participants = request.POST.get('maximum_no_of_participants')
    tournament_description = request.POST.get('tournament_description')
    tournament_short_description = request.POST.get('tournament_short_description', '')
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

    if tournament.organizer.user != user:
        return Response({"error": "You are not authorized to update this Tournament"}, status=status.HTTP_403_FORBIDDEN)

    tournament.tournament_name = tournament_name
    tournament.tournament_logo = tournament_logo
    tournament.tournament_banner = tournament_banner
    tournament.tournament_mode = tournament_mode
    tournament.location = location
    tournament.tournament_participants = tournament_participants
    tournament.is_free = is_free
    tournament.tournament_fee = tournament_fee
    tournament.maximum_no_of_participants = maximum_no_of_participants
    tournament.tournament_description = tournament_description
    tournament.tournament_short_description = tournament_short_description
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
    tournament_id = request.GET.get("id")
    tournament = Tournament.objects.get(id=tournament_id)
    sponsor = TournamentSponsor.objects.filter(tournament = tournament)
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
    tournament_id = request.GET.get("id")
    tournament = Tournament.objects.get(id=tournament_id)
    faq = TournamentFAQ.objects.filter(tournament = tournament)
    serializer = TournamentFAQSerializer(faq)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tournament_faq(request):
    faq_id = request.POST.get('id')
    value = request.POST.get('value')
    heading = request.POST.get('heading')
    detail = request.POST.get('detail')

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tournament_stream(request):
    user = request.user
    if user.role != "Organizer":
        tournament_id = request.POST.get('id')
        stream_name = request.POST.get('stream_name')
        url = request.POST.get('url')

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)
        tournament_stream = TournamentStreams.objects.create(
            tournament = tournament,
            stream_name = stream_name,
            url = url
        )
        tournament_stream.save()
        return Response({"success": "Tournament Stream created successfully"})
    else:
        return Response({"error": "Unauthorized to create the Tournament Stream"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def tournament_stream(request):
    tournament_id = request.GET.get("id")
    tournament = Tournament.objects.get(id=tournament_id)
    tournament_stream= TournamentStreams.objects.filter(tournament=tournament)
    serializer = TournamentStreamsSerializer(tournament_stream, many=True)
    return Response({"tournament_streams": serializer.data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournament_stream_list(request):
    pk = request.GET.get('id')
    stream = TournamentStreams.objects.get(id = pk)
    serializer = TournamentStreamsSerializer(stream)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_tournament_stream(request):
    stream_id = request.POST.get('id')
    user = request.user

    if user.role == "Organizer":
        stream_name = request.POST.get('stream_name')
        url = request.POST.get('url')

        try:
            stream = TournamentStreams.objects.get(id=stream_id)
        except TournamentStreams.DoesNotExist:
            return Response({"error": "Tournament stream not found"})
        stream.stream_name = stream_name
        stream.url = url
        stream.save()

        return Response({"success": "Tournament stream updated successfully"})
        
    else:
        return Response({"error": "Unauthorized to update the tournament stream"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tournament_stream(request):
    stream_id = request.GET.get("id")
    user = request.user

    if user.role == "Organizer":
        tournament_stream = TournamentStreams.objects.get(id=stream_id)
        tournament_stream.delete()
        return Response({"success": "TournamentStream deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the tournament stream"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stage(request):
    user = request.user
    
    if user.role == "Organizer":
        elimination_mode_id = request.POST.get('elimination_mode_id')
        stage_number = request.POST.get('stage_number')
        no_of_participants = request.POST.get('no_of_participants')
        no_of_groups = request.POST.get('no_of_groups')
        stage_name = request.POST.get('stage_name')
        tournament_id = request.POST.get('tournament_id')

        try:
            elimination_mode = EliminationMode.objects.get(id=elimination_mode_id)
            tournament = Tournament.objects.get(id=tournament_id)
        except (EliminationMode.DoesNotExist, Tournament.DoesNotExist):
            return Response({"error": "Invalid elimination mode or tournament"}, status=status.HTTP_404_NOT_FOUND)
        stage = Stage.objects.create(
            stage_elimation_mode=elimination_mode,
            stage_number=stage_number,
            no_of_participants=no_of_participants,
            no_of_groups=no_of_groups,
            stage_name=stage_name,
            tournament=tournament
        )
        stage.save()
        return Response({"success": "Stage created successfully"})
        
    else:
        return Response({"error": "Unauthorized to create a stage"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def stage_list(request):
    stages = Stage.objects.all()
    serializer = StageSerializer(stages, many=True)
    return Response({"stages": serializer.data})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stage(request):
    tournament_id = request.GET.get("id")
    tournament = Tournament.objects.get(id=tournament_id)
    stages = Stage.objects.filter(tournament=tournament)
    serializer = StageSerializer(stages, many=True)
    return Response({"stages": serializer.data})


@api_view(['GET'])
def stage_list(request):
    pk = request.GET.get('id')
    try:
        stage = Stage.objects.get(id=pk)
        serializer = StageSerializer(stage)
        return Response(serializer.data)
    except Stage.DoesNotExist:
        return Response({"error": "Stage not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_stage(request):
    stage_id = request.GET.get('id')
    user = request.user

    if user.role == "Organizer":
        stage_number = request.POST.get('stage_number')
        no_of_participants = request.POST.get('no_of_participants')
        no_of_groups = request.POST.get('no_of_groups')
        stage_name = request.POST.get('stage_name')

        try:
            stage = Stage.objects.get(id=stage_id)
        except (Stage.DoesNotExist):
            return Response({"error": "Invalid stage"})
        stage.stage_number = stage_number
        stage.no_of_participants = no_of_participants
        stage.no_of_groups = no_of_groups
        stage.stage_name = stage_name
        stage.save()
        return Response({"success": "Stage updated successfully"})
    
    else:
        return Response({"error": "Unauthorized to update the stage"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stage(request):
    stage_id = request.GET.get("id")
    user = request.user

    if user.role == "Organizer":
        try:
            stage = Stage.objects.get(id=stage_id)
        except Stage.DoesNotExist:
            return Response({"error": "Stage not found"})
        stage.delete()
        return Response({"success": "Stage deleted successfully"})
        
    else:
        return Response({"error": "Unauthorized to delete the stage"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def registered_teams(request):
    tournament_id = request.GET.get("id")
    
    user = request.user

    if user.role == "Organizer":
        tournament = Tournament.objects.get(id=tournament_id)
        registrations = TeamTournamentRegistration.objects.filter(tournament__in=tournament)
        serializer = TeamTournamentRegistrationSerializer(registrations, many=True)
        return Response({"registrations": serializer.data})
    else:
        return Response({"error": "Unauthorized to view registered teams"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def open_registration(request):
    tournament_id = request.POST.get('id')
    registration_opening_date = request.POST.get('registration_opening_date')
    registration_closing_date = request.POST.get('registration_closing_date')

    try:
        tournament = Tournament.objects.get(id=tournament_id)
    except Tournament.DoesNotExist:
        return Response({"error": "Tournament does not exist"}, status=status.HTTP_404_NOT_FOUND)

    is_free = request.POST.get('is_free') 

    if is_free == 'true': 
        tournament.is_free = True
        tournament.tournament_fee = 0
    else:
        tournament.is_free = False
        tournament.tournament_fee = 100 

    tournament.registration_opening_date = registration_opening_date
    tournament.registration_closing_date = registration_closing_date
    tournament.save()

    return Response({"success": "Registration opened for the tournament"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_team(request):
    user = request.user
    tournament_id = request.POST.get('tournament_id')
    team_id = request.POST.get('team_id')
    registration_fee = request.POST.get('registration_fee')
    registration_status = request.POST.get('registration_status', 'Ongoing Review')
    payment_method = request.POST.get('payment_method', 'Other')
    current_stage_id = request.POST.get('current_stage_id')

    try:
        tournament = Tournament.objects.get(id=tournament_id)
        team = Team.objects.get(id=team_id)
        current_stage = Stage.objects.get(id=current_stage_id)
    except (Tournament.DoesNotExist, Team.DoesNotExist):
        return Response({"error": "Invalid tournament or team"}, status=404)

    if user.role == "Organization":
        if open_registration(tournament):
            registration = TeamTournamentRegistration.objects.create(
                tournament=tournament,
                team=team,
                registration_fee=registration_fee,
                registration_status=registration_status,
                payment_method=payment_method,
                current_stage=current_stage
            )
            registration.save()
            return Response({"success": "Team registered successfully"})
        else:
            return Response({"error": "Cannot register team. Registration is not open or some conditions are not met."})
    else:
        return Response({"error": "Unauthorized to register a team"})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_team_registration(request):
    registration_id = request.GET.get('id')
    user = request.user

    if user.role == "Organizer":
        team_id = request.POST.get('team_id')
        registration_fee = request.POST.get('registration_fee')
        registration_status = request.POST.get('registration_status')
        payment_method = request.POST.get('payment_method')
        current_stage_id = request.POST.get('id')

        try:
            team_registration = TeamTournamentRegistration.objects.get(id=registration_id)
            team = Team.objects.get(id=team_id)
            current_stage = Stage.objects.get(id=current_stage_id) 
        except (TeamTournamentRegistration.DoesNotExist, Team.DoesNotExist, Stage.DoesNotExist):
            return Response({"error": "Invalid team registration, team, or current stage"})

        team_registration.team = team
        team_registration.registration_fee = registration_fee
        team_registration.registration_status = registration_status
        team_registration.payment_method = payment_method
        team_registration.current_stage = current_stage

        team_registration.save()
        return Response({"success": "Team registration updated successfully"})
    else:
        return Response({"error": "Unauthorized to update the team registration"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_team_registration(request):
    registration_id = request.GET.get("id")
    user = request.user

    if user.role == "Organization":
        try:
            team_registration = TeamTournamentRegistration.objects.get(id=registration_id)
        except TeamTournamentRegistration.DoesNotExist:
            return Response({"error": "Team registration not found"})
        team_registration.delete()
        return Response({"success": "Team registration deleted successfully"})
    else:
        return Response({"error": "Unauthorized to delete the team registration"}, status=status.HTTP_401_UNAUTHORIZED)