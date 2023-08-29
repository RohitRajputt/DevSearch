from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Profile
from .serializers import ProfileSerializer

@api_view(['GET'])
def getRoutes(request):
    routes=[
        "GET /api",
        'GET /api/profiles',
        'GET /api/profiles/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProfile(request,  pk):
    profile = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)