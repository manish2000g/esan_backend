from django.db import models
from ckeditor.fields import RichTextField
from account.models import  Organization, Organizer, Player

class Team(models.Model):
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    captain = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='captain_of')
    members = models.ManyToManyField(Player, related_name='member_of', blank=True)
    team_manager = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='manager_of')

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-start_date',)

class Tournament(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = RichTextField()
    registration_end_date = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    team = models.ManyToManyField(Team, related_name='teams', blank=True)
    player = models.ManyToManyField(Player, related_name='players', blank=True)

    def __str__(self):
        return self.name

class BannerImage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tournament_banners/')

    def __str__(self):
        return f"{self.tournament.name} Banner"
    
class PrizePool(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.TextField(max_length=20)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    extras = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.tournament.name} - {self.extras}: {self.amount}"


class Registration(models.Model):
    REGISTRATION_TYPE_CHOICES = [
        ('TEAM', 'Team'),
        ('PLAYER', 'Player'),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    registration_type = models.CharField(choices=REGISTRATION_TYPE_CHOICES, max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    captain = models.ManyToManyField(Player, related_name='captain')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        if self.registration_type == 'TEAM':
            return f"{self.team} registered for {self.tournament}"
        else:
            return f"{self.player} registered for {self.tournament}"

# class Registration(models.Model):
#     team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
#     team_logo = models.ImageField(upload_to='team_logos/')
#     captain = models.ManyToManyField(Player, related_name='captain')
#     players = models.ManyToManyField(Player, related_name='registrations', blank=True)
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return self.team_name

class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SWISS SYSTEM', 'Swiss system'),
        ('LEAGUE', 'League'),
        ('ROUND ROBINS', 'Round Robins'),
        ('BATTLE ROYAL', 'Battle Royal')
    ]
    GAME_MODE_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]
    GAME_PLATFORM = [
        ('mobile', 'Mobile'),
        ('console', 'Console'),
        ('pc', 'PC')
    ]
    game_platform = models.CharField(max_length=15, choices=GAME_PLATFORM)
    name = models.CharField(max_length=300)
    game_type = models.CharField(max_length=20, choices=GAME_TYPE_CHOICES)
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    description = RichTextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.game_type} - {self.tournament.name}"

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

   
class TournamentBracket(models.Model):
    TOURNAMENT_TYPE_CHOICES = [
        ('single_elimination', 'Single Elimination'),
        ('double_elimination', 'Double Elimination'),
        ('round_robin', 'Round Robin'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='brackets')
    type = models.CharField(max_length=50, choices=TOURNAMENT_TYPE_CHOICES)
    number_of_rounds = models.PositiveSmallIntegerField()
    rounds_per_match = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='won_brackets')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='lost_brackets')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    number_of_teams = models.PositiveSmallIntegerField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['number_of_rounds']

    def __str__(self):
        return f'{self.type} Bracket for {self.tournament}'
    
class Round(models.Model):
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.bracket.tournament.name} - Round {self.round_number}"   

class Group(models.Model):
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    group_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.bracket.tournament.name} - Group {self.group_number}: {self.name}"

class Match(models.Model):
    MATCH_TYPE_CHOICES = (
        ('DUEL', 'Duel'),
        ('FFA', 'Free for All'),
    )
    MATCH_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    match_type = models.CharField(max_length=4, choices=MATCH_TYPE_CHOICES)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    match_number = models.IntegerField()
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_team_1')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_team_2')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    status = models.CharField(max_length=20, choices=MATCH_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.player_1.user.username} vs {self.player_2.user.username} - {self.game.tournament.name}"

class DuelMatch(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='duel_matches_player1')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='duel_matches_player2')
    score_1 = models.PositiveIntegerField(blank=True, null=True)
    score_2 = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.player_1.user.username} vs {self.player_2.user.username} - {self.match.game.tournament.name}"
    
class FFAMatch(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name='ffa_matches_players')
    scores = models.ManyToManyField(Player, through='FFAScore')

    def __str__(self):
        return f"FFA Match - {self.match.game.tournament.name}"

class FFAScore(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(FFAMatch, on_delete=models.CASCADE)
    score = models.IntegerField()

    # def __str__(self):
    #     return f"{}"

class Schedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='schedule')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='schedule')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
class Result(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="results")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_result")
    created_at = models.DateTimeField(auto_now_add=True)
    RESULT_CHOICES = [
        ('player_1', 'Player 1 wins'),
        ('player_2', 'Player 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    duel_score_1 = models.PositiveIntegerField(null=True, blank=True)
    duel_score_2 = models.PositiveIntegerField(null=True, blank=True)
    ffa_scores = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.tournament} - {self.result}"

class Sponsor(models.Model):
    SPONSOR_TYPE_CHOICES = [
        ('title', 'Title Sponsor'),
        ('presenting', 'Presenting Sponsor'),
        ('official', 'Official Sponsor'),
        ('media', 'Media Partner'),
        ('support', 'Support Sponsor'),
        ('technical', 'Technical Sponsor'),
        ('gaming', 'Gaming Partner'),
        ('food_and_beverages', 'Food and Beverages Sponsor'),
        ('venue', 'Venue Sponsor'),
        ('merchandise', 'Merchandise Partner'),
        ('broadcast', 'Broadcast Partner'),
    ]
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/', null=True)
    type = models.CharField(max_length=40, choices=SPONSOR_TYPE_CHOICES)
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE, related_name='sponsor')
    def __str__(self):
        return self.name
    

class LivePage(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True)
    chat_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.tournament.name

class Announcement(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)



