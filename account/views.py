from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import BlogWriter, Organization, Organizer, Player, UserProfile

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        )

@api_view(['POST'])
def CreateUserProfile(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    is_player = request.POST.get('is_player', "False") == "True"
    is_blog_writer = request.POST.get('is_blog_writer', "False") == "True"
    is_organizer = request.POST.get('is_organizer', "False") == "True"
    is_organization = request.POST.get('is_organization', "False") == "True"

    if is_player:
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='player')
        name = request.POST['name']
        country = request.POST['country']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES.get('profile_picture', None)
        player = Player.objects.create(user=user, name=name, country=country, phone_number=phone_number, profile_picture=profile_picture)
        player.save()

    elif is_blog_writer:
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='blog_writer')
        name = request.POST['name']
        bio = request.POST['bio']
        website = request.POST['website']
        email = request.POST['email']
        profile_picture = request.FILES.get('profile_picture', None)
        blog_writer = BlogWriter.objects.create(user=user, name=name, bio=bio, website=website, email=email, profile_picture=profile_picture)
        blog_writer.save()

    elif is_organizer:
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='organizer')
        name = request.POST['name']
        description = request.POST['description']
        website = request.POST['website']
        email = request.POST['email']
        logo = request.FILES.get('logo', None)
        organizer = Organizer.objects.create(user=user, name=name, description=description, website=website, email=email, logo=logo)
        organizer.save()

    elif is_organization:
        user = UserProfile.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name, role='organization')
        organization_name = request.POST['organization_name']
        description = request.POST['description']
        website = request.POST['website']
        email = request.POST['email']
        address = request.POST['address']
        logo = request.FILES.get('logo', None)
        organization = Organization.objects.create(user=user, organization_name=organization_name, description=description, website=website, email=email, address=address, logo=logo)
        organization.save()

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    })



