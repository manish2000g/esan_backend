from django.db import models
from django.contrib.auth.models import User

    
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='media/images/player_profile_pictures/')
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BlogWriter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=500)
    profile_picture = models.ImageField(upload_to='media/images/blog_profile_pictures/')
    website = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='media/images/organizer_logos/')
    description = models.TextField(max_length=500)
    website = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='media/images/organization_logos/')
    description = models.TextField(max_length=500)
    website = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.organization_name
    
