from rest_framework import serializers

from account.models import Organizer
from .models import Tournament, Registration, Schedule, Participant, Match, LivePage, Announcement

from rest_framework import serializers
from .models import Sponsor, Tournament, Post, Registration, Schedule, Participant, Match, LivePage, Announcement
from account.serializers import OrganizationSerializer, OrganizerSerializer, PlayerSerializer

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class TournamentSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer()
    sponsors = SponsorSerializer(many=True)

    class Meta:
        model = Tournament
        fields = '__all__'

    def create(self, validated_data):
        organizer_data = validated_data.pop('organizer')
        sponsors_data = validated_data.pop('sponsors')
        tournament = Tournament.objects.create(**validated_data)
        organizer = Organizer.objects.create(tournament=tournament, **organizer_data)
        sponsors = [Sponsor.objects.create(tournament=tournament, **sponsor_data) for sponsor_data in sponsors_data]
        tournament.sponsors.set(sponsors)
        return tournament

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    captain = PlayerSerializer()
    players = PlayerSerializer(many=True)
    tournament = TournamentSerializer()

    class Meta:
        model = Registration
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()
    team1 = RegistrationSerializer()
    team2 = RegistrationSerializer()
    winner = RegistrationSerializer()

    class Meta:
        model = Schedule
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()
    player = PlayerSerializer()

    class Meta:
        model = Participant
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    team_1 = OrganizationSerializer()
    team_2 = OrganizationSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = Match
        fields = '__all__'

class LivePageSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = LivePage
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = Announcement
        fields = '__all__'

