from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import BlogWriter, Game, Organization, Organizer, Player, UserProfile, Team
from rest_framework import status
from .serializers import GameSerializer, TeamSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user":{
                'user': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        })

@api_view(['POST'])
def CreateUserProfile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    user_type = request.POST.get('user_type', "is_player")

    if user_type=="is_player":
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='player')
        player = Player.objects.create(user=user)
        player.save()

    elif user_type=="is_blog_writer":
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='blog_writer')
        blog_writer = BlogWriter.objects.create(user=user)
        blog_writer.save()

    elif user_type=="is_organizer":
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='organizer')
        organizer = Organizer.objects.create(user=user)
        organizer.save()

    elif user_type=="is_organization":
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='organization')
        organization_name = request.POST['organization_name']
        organization = Organization.objects.create(user=user, organization_name=organization_name)
        organization.save()

    return Response({
        "success":"User Created Sucessfully"
    },status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserProfile(request):
    user = request.user
    return Response({
        "user":{
            'user': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role
        }
    })

@api_view(['GET', 'POST'])
def team_list(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


