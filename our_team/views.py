from rest_framework.response import Response
from our_team.models import OurTeam
from our_team.serializers import OurTeamSerializer
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def OurTeams(request):
    teams = OurTeam.objects.all()
    serializers = OurTeamSerializer(teams, many=True)
    return Response({"teams": serializers.data})

@api_view(['POST'])
def CreateOurTeam(request):
    name = request.POST.get('name')
    post = request.POST.get('post')
    image = request.POST.get('image')
    facebook_link = request.POST.get('facebook_link')
    instagram_link = request.POST.get('instagram_link')
    twitch_link = request.POST.get('twitch_link')
    twitter_link = request.POST.get('twitter_link')
    discord_link = request.POST.get('discord_link')
    linkedin_link = request.POST.get('linkedin_link')

    team = OurTeam.objects.create(
        name = name,
        post = post,
        image = image,
        facebook_link = facebook_link,
        instagram_link = instagram_link,
        twitch_link = twitch_link,
        twitter_link = twitter_link,
        discord_link = discord_link,
        linkedin_link = linkedin_link
    ) 
    team.save()
    return Response({"success": "Team member Created Successfully"},status=status.HTTP_200_OK)

    
@api_view(['PUT'])
def UpdateOurTeam(request):
    pk = request.GET.get("id")
    team = OurTeam.objects.get(pk=pk)
    name = request.POST.get('name')
    post = request.POST.get('post')
    image = request.POST.get('image')
    facebook_link = request.POST.get('facebook_link')
    instagram_link = request.POST.get('instagram_link')
    twitch_link = request.POST.get('twitch_link')
    twitter_link = request.POST.get('twitter_link')
    discord_link = request.POST.get('discord_link')
    linkedin_link = request.POST.get('linkedin_link')

    team.name = name
    team.post = post
    team.image = image
    team.facebook_link = facebook_link
    team.instagram_link = instagram_link
    team.twitch_link = twitch_link
    team.twitter_link = twitter_link
    team.discord_link = discord_link
    team.linkedin_link = linkedin_link

    team.save()
    return Response({"success": "Team member Updated Successfully"})

@api_view(['Delete'])
def DeleteOurTeam(request):
    pk = request.GET.get("id")
    team = OurTeam.objects.get(pk=pk)
    team.delete()
    return Response({"Team member Deleted Successfully"})
