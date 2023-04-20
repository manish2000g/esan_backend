from django.db import models
from ckeditor.fields import RichTextField
from account.models import  Organizer, Player, Team
    
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class BannerImage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tournament_banners/')

    def __str__(self):
        return f"{self.tournament.name} Banner"
    
class PrizePool(models.Model):
    TITLE_CHOICES = [
        ('1st', '1st Place'),
        ('2nd', '2nd Place'),
        ('3rd', '3rd Place'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    extras = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tournament.name} - {self.extras}: {self.amount}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)
    team_logo = models.ImageField(upload_to='team_logos/')
    captain = models.ManyToManyField(Player, related_name='captain')
    players = models.ManyToManyField(Player, related_name='registrations', blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.team_name

class Game(models.Model):
    GAME_TYPE_CHOICES = [
        ('SOLO', 'Solo'),
        ('DUO', 'Duo'),
        ('TEAM', 'Team'),
    ]
    GAME_MODE_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
    ]
    name = models.CharField(max_length=300)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=10, choices=GAME_TYPE_CHOICES)
    game_mode = models.CharField(max_length=10, choices=GAME_MODE_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    rules = RichTextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.game_type()} - {self.tournament.name}"

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Match(models.Model):
    MATCH_TYPE_CHOICES = (
        ('DUEL', 'Duel'),
        ('FFA', 'Free for All'),
    )
    match_type = models.CharField(max_length=4, choices=MATCH_TYPE_CHOICES)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
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
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.player_1.name} vs {self.player_2.name} - {self.game.tournament.name}"

class DuelMatch(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='duel_matches_player1')
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='duel_matches_player2')
    score_1 = models.PositiveIntegerField(blank=True, null=True)
    score_2 = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.player_1.name} vs {self.player_2.name} - {self.match.game.tournament.name}"
    
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

    
class TournamentBracket(models.Model):
    TOURNAMENT_BRACKET_CHOICES = [
        ('WINNER', 'Winner'),
        ('LOSER', 'Loser'),
        ('SEMIFINALS', 'Semifinals'),
        ('FINALS', 'Finals'),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='brackets')
    name = models.CharField(max_length=50, choices=TOURNAMENT_BRACKET_CHOICES)
    round = models.PositiveSmallIntegerField()
    matches = models.ManyToManyField(Match, related_name='brackets')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='won_brackets')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='lost_brackets')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    num_teams = models.PositiveSmallIntegerField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['round']

    def __str__(self):
        return f'{self.name} Bracket for {self.tournament}'

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



