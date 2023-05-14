from rest_framework.response import Response
from our_team.models import OurTeam
from our_team.serializers import OurTeamSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def OurTeams(request):
    teams = OurTeam.objects.all()
    serializers = OurTeamSerializer(teams, many=True)
    return Response(serializers.data)