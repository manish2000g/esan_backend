from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import BlogWriter, Game, Organization, Organizer, Player, UserProfile
from rest_framework import status
from .serializers import GameSerializer,UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.core.mail import send_mail

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
def VerifyUserProfile(request):
    userid = request.GET.get("user")
    userpr = UserProfile.objects.get(id=userid)
    userpr.is_verified = True
    userpr.save()
    return Response({"detail":"Verified Sucessfully"})
 
@api_view(['POST'])
def CreateUserProfile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    user_type = request.POST.get('user_type', "is_player")

    # Check if email already exists
    if UserProfile.objects.filter(email=email).exists():
        return Response({'detail': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username already exists
    if UserProfile.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if all required fields are present
    if not all([first_name, last_name, email, password, username, user_type]):
        return Response({'detail': 'All required fields are not present'}, status=status.HTTP_400_BAD_REQUEST)

    if user_type=="is_player":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Player')
        player = Player.objects.create(user=user)   
        player.save()

    elif user_type=="is_blog_writer":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Blog Writer')
        blog_writer = BlogWriter.objects.create(user=user)
        blog_writer.save()

    elif user_type=="is_organizer":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Organizer')
        organizer = Organizer.objects.create(user=user)
        organizer.save()

    elif user_type=="is_organization":
        user = UserProfile.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, role='Organization')
        organization_name = request.POST['organization_name']
        organization = Organization.objects.create(user=user, organization_name=organization_name)
        organization.save()

    message = f'Hello,\n\nThank you for signing up for ESAN! To get started, please click on the following link to verify your account : https://esan.hikingbees.com/verify-user-profile/?user={user.id} \n\nBest regards,\nESAN'

    send_mail(
        'Verify Your ESAN Account',
        message,
        'vishaldhakal9696@gmail.com',
        [email],
        fail_silently=False,
    )
    return Response({
        "success":"User Created Sucessfully"
    },status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserProfile(request):
    user = request.user
    if user.is_verified:
        data = {
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            }
        }

        if user.role == 'Player':
            player = Player.objects.get(user=user)
            data['player'] = {
                'id': player.id,
                'profile_picture': player.profile_picture.url if player.profile_picture else None,
                'country': player.country,
                'phone_number': player.phone_number
            }

        elif user.role == 'Blog Writer':
            blog_writer = BlogWriter.objects.get(user=user)
            data['blog_writer'] = {
                'id': blog_writer.id,
                'bio': blog_writer.bio,
                'profile_picture': blog_writer.profile_picture.url if blog_writer.profile_picture else None,
                'website': blog_writer.website
            }

        elif user.role == 'Organizer':
            organizer = Organizer.objects.get(user=user)
            data['organizer'] = {
                'id': organizer.id,
                'logo': organizer.logo.url if organizer.logo else None,
                'description': organizer.description,
                'website': organizer.website
            }

        elif user.role == 'Organization':
            organization = Organization.objects.get(user=user)
            data['organization'] = {
                'id': organization.id,
                'organization_name': organization.organization_name,
                'logo': organization.logo.url if organization.logo else None,
                'description': organization.description,
                'website': organization.website,
                'address': organization.address
            }

        return Response(data)
    else:
        return Response({"detail":"User not verified"},status=403)

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


@api_view(['GET', 'POST'])
def GetUsers(request):
    users = UserProfile.objects.all()
    users_serializer = UserProfileSerializer(users,many=True)
    return Response({"users":users_serializer.data})


