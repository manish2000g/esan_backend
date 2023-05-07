from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class UserProfile(AbstractUser):
    role_choices = (
        ('Player', 'Player'),
        ('Organization', 'Organization'),
        ('Organizer', 'Organizer'),
        ('Blog Writer', 'Blog Writer'),
        ('Admin', 'Admin'),
    )
    
    status_choices = (
        ('Active', 'Active'),
        ('Banned', 'Banned'),
    )
    
    role = models.CharField(max_length=15, choices=role_choices)
    avatar = models.ImageField(blank=True)
    status = models.CharField(max_length=15, choices=status_choices,default="Active")
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=500,blank=True)
    nationality = models.CharField(max_length=100,default="Nepal")
    bio = models.TextField(blank=True)
    facebook_link = models.CharField(max_length=250,blank=True)
    instagram_link = models.CharField(max_length=250,blank=True)
    twitch_link = models.CharField(max_length=250,blank=True)
    discord_link = models.CharField(max_length=250,blank=True)
    reddit_link = models.CharField(max_length=250,blank=True)
    website_link = models.CharField(max_length=250,blank=True)
    youtube_link = models.CharField(max_length=250,blank=True)
    twitter_link = models.CharField(max_length=250,blank=True)
    linkedin_link = models.CharField(max_length=250,blank=True)

    def __str__(self) -> str:
        return self.username
    

class Player(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class BlogWriter(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    website = models.URLField(max_length=200,blank=True)
    position = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return self.user.username

class Organizer(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255,unique=True,blank=True)

    def __str__(self):
        return self.user.username

class Organization(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255,unique=True,blank=True)

    def __str__(self):
        return self.organization_name
    
class Game(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='meddia/images/game_by_admin')

    def __str__(self):
        return self.name


