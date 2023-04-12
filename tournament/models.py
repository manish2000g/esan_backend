from django.db import models
from django.db import models
from account.models import Organization, Organizer, Player


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='sponsor_logos/', null=True)

    def __str__(self):
        return self.name
    
class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rules = models.TextField()
    bracket = models.TextField()
    banner_image = models.ImageField(upload_to='tournament_banners/', null=True)
    sponsors = models.ManyToManyField(Sponsor, blank=True)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    team_name = models.CharField(max_length=200)
    team_logo = models.ImageField(upload_to='team_logos/')
    captain = models.ForeignKey(Player, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name='registrations', blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

class Schedule(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    team1 = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='team2_matches')
    winner = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='winner_matches')
    is_finished = models.BooleanField(default=False)

class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

class Match(models.Model):
    team_1 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='match_team_1')
    team_2 = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='match_team_2')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    match_date = models.DateTimeField()
    score_team_1 = models.IntegerField(null=True, blank=True)
    score_team_2 = models.IntegerField(null=True, blank=True)

class LivePage(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    video_url = models.URLField(null=True, blank=True)
    chat_url = models.URLField(null=True, blank=True)

class Announcement(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)