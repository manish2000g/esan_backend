from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserProfile(AbstractUser):
    role_choices = (
        ('player', 'Player'),
        ('organization', 'Organization'),
        ('organizer', 'Organizer'),
        ('blog_writer', 'Blog Writer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=15, choices=role_choices)

    def __str__(self) -> str:
        return self.username
    
class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/images/player_profile_pictures/',blank=True)
    country = models.CharField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.name

class BlogWriter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(upload_to='media/images/blog_profile_pictures/',blank=True)
    website = models.URLField(max_length=200,blank=True)

    def __str__(self):
        return self.name

class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='media/images/organizer_logos/',blank=True)
    description = models.TextField(max_length=500,blank=True)
    website = models.URLField(max_length=200,blank=True)

    def __str__(self):
        return self.name

class Organization(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='media/images/organization_logos/',blank=True)
    description = models.TextField(max_length=500,blank=True)
    website = models.URLField(max_length=200,blank=True)
    address = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.organization_name
    
class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='meddia/images/game_by_admin')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    captain = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='captain_of')
    members = models.ManyToManyField(Player, related_name='member_of', blank=True)
    team_manager = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='manager_of')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
