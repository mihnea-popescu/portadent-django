from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import re_path
from rest_framework.decorators import api_view
from api.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(instance=request.user)
    return Response({"user": serializer.data})


urlpatterns = [
    re_path("current", get_current_user)
]
