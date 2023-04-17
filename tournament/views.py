
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Sponsor, Tournament, Registration, Participant, LivePage, Announcement, Match, TournamentBracket
from .serializers import SponsorSerializer, TournamentBracketSerializer, TournamentSerializer, RegistrationSerializer, MatchSerializer, ParticipantSerializer, LivePageSerializer, AnnouncementSerializer
from rest_framework import status

@api_view(['GET'])
def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    serializer = SponsorSerializer(sponsor)
    return Response(serializer.data)

@api_view(['POST'])
def create_tournament(request):
    serializer = TournamentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_tournament(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    tournament.delete()
    return Response(status=204)

@api_view(['GET'])
def tournament_list(request):
    tournaments = Tournament.objects.all()
    serializer = TournamentSerializer(tournaments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tournament_detail(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    serializer = TournamentSerializer(tournament)
    return Response(serializer.data)

@api_view(['POST'])
def create_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    serializer = RegistrationSerializer(registration, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk)
    registration.delete()
    return Response(status=204)

@api_view(['POST'])
def create_participant(request):
    serializer = ParticipantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
    return Response(status=204)

@api_view(['GET'])
def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    serializer = MatchSerializer(match)
    return Response(serializer.data)

@api_view(['POST'])
def create_match(request):
    serializer = MatchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    serializer = MatchSerializer(match, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    match.delete()
    return Response(status=204)


@api_view(['GET', 'POST'])
def tournament_bracket_list(request):
    """
    List all tournament brackets, or create a new bracket.
    """
    if request.method == 'GET':
        brackets = TournamentBracket.objects.all()
        serializer = TournamentBracketSerializer(brackets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TournamentBracketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def tournament_bracket_detail(request, pk):
    """
    Retrieve, update or delete a tournament bracket.
    """
    bracket = get_object_or_404(TournamentBracket, pk=pk)

    if request.method == 'GET':
        serializer = TournamentBracketSerializer(bracket)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TournamentBracketSerializer(bracket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bracket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def livepage_detail(request, pk):
    livepage = get_object_or_404(LivePage, pk=pk)
    serializer = LivePageSerializer(livepage)
    return Response(serializer.data)

@api_view(['PUT'])
def update_livepage(request, pk):
    livepage = get_object_or_404(LivePage, pk=pk)
    serializer = LivePageSerializer(livepage, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    serializer = AnnouncementSerializer(announcement)
    return Response(serializer.data)

@api_view(['POST'])
def create_announcement(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
