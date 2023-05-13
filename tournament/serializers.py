from rest_framework import serializers
from .models import (EliminationMode, Game, Team, Event, EventFAQ, EventSponsor,
                     Tournament, TournamentFAQ, TournamentSponsor, TournamentStreams, Stage,SoloTournamentRegistration,TeamTournamentRegistration,SoloGroup,TeamGroup,SoloMatch,TeamMatch)

class EliminationModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EliminationMode
        fields = ('id', 'elimination_mode')

class GameSerializer(serializers.ModelSerializer):
    elimination_modes = EliminationModeSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'game_name', 'game_image', 'game_type', 'elimination_modes')

class TeamSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)
    manager = serializers.StringRelatedField()
    organization = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_image', 'game', 'team_type', 'players', 'manager', 'organization')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'organizer', 'event_name', 'event_description', 'event_start_date', 'event_end_date')

class EventFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFAQ
        fields = ('id', 'event', 'value', 'heading', 'detail')

class EventSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSponsor
        fields = ('id', 'event', 'sponsor_name', 'sponsorship_category', 'sponsor_banner')

class TournamentFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentFAQ
        fields = ('id', 'tournament', 'value', 'heading', 'detail')

class TournamentSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    tournament_streams = serializers.StringRelatedField(many=True)
    tournament_sponsors = serializers.StringRelatedField(many=True)
    tournament_faqs = TournamentFAQSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ('id', 'organizer', 'tournament_name', 'tournament_logo', 'tournament_mode', 'tournament_participants',
                  'is_free', 'tournament_fee', 'maximum_no_of_participants', 'game', 'tournament_description',
                  'tournament_rules', 'tournament_prize_pool', 'registration_opening_date', 'registration_closing_date',
                  'tournament_start_date', 'tournament_end_date', 'created_at', 'updated_at', 'is_published',
                  'is_registration_enabled', 'accept_registration_automatic', 'contact_email', 'discord_link',
                  'tournament_streams', 'tournament_sponsors', 'tournament_faqs')

class TournamentStreamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStreams
        fields = ('id', 'tournament', 'stream_name', 'url')

class TournamentSponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentSponsor
        fields = ('id', 'tournament', 'sponsor_name', 'sponsorship_category', 'sponsor_logo', 'sponsor_link', 'sponsor_banner')

class StageSerializer(serializers.ModelSerializer):
    stage_elimation_mode = EliminationModeSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = Stage
        fields = ('id', 'stage_elimation_mode', 'stage_number', 'no_of_participants', 'no_of_groups', 'stage_name', 'tournament')


class SoloTournamentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloTournamentRegistration
        fields = '__all__'


class TeamTournamentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTournamentRegistration
        fields = '__all__'


class SoloGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloGroup
        fields = '__all__'
        
class TeamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamGroup
        fields = '__all__'


class SoloMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloMatch
        fields = '__all__'

class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'
