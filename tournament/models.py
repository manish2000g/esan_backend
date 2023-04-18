from django.db import models
from ckeditor.fields import RichTextField
from account.models import Organization, Organizer, Player
    
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=300)
    rules = RichTextField()
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class BannerImage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tournament_banners/')

    def __str__(self):
        return f"{self.tournament.name} Banner"
    
class PrizePool(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    extras = models.CharField(max_length=100, choices=[
        ('gift_voucher', 'Gift Voucher'),
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('tour ticket', 'Tour Ticket'),
    ], default='gift_voucher')

    def __str__(self):
        return f"{self.tournament.name} - {self.extras}: {self.amount}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    team_name = models.ForeignKey(Organization, on_delete=models.CASCADE)
    team_logo = models.ImageField(upload_to='team_logos/')
    captain = models.ForeignKey(Player, on_delete=models.CASCADE)
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
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    game_type = models.CharField(max_length=10, choices=GAME_TYPE_CHOICES)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.game_type()} - {self.tournament.name}"

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    team_1 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='match_team_1')
    team_2 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='match_team_2')
    is_completed = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.team_1.organization_name} vs {self.team_2.organization_name} - {self.game.tournament.name}"
 

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
    winner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='won_brackets')
    loser = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, related_name='lost_brackets')

    class Meta:
        ordering = ['round']

    def __str__(self):
        return f'{self.name} Bracket for {self.tournament}'
    
class Result(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="results")
    team1 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="results_team1")
    team2 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="results_team2")
    score1 = models.PositiveIntegerField()
    score2 = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    RESULT_CHOICES = [
        ('team_1', 'Team 1 wins'),
        ('team_2', 'Team 2 wins'),
        ('draw', 'Draw'),
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    def __str__(self):
        return f"{self.tournament} - {self.result}"

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/', null=True)
    tournament = models.ForeignKey(Tournament,on_delete=models.CASCADE, related_name='sponsor')
    def __str__(self):
        return self.name

class LivePage(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
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



