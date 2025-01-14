from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import path
from rest_framework.decorators import api_view
from api.serializers import ScanPhotoSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import ScanPhoto, ScanStatusType


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_scan_photo(request):
    serializer = ScanPhotoSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if serializer.validated_data['scan'].status != ScanStatusType.INITIALIZED.value:
        return Response({"details": "This scan does not accept any photos."}, status=status.HTTP_400_BAD_REQUEST)

    previous_scan_photo = ScanPhoto.objects.filter(type=serializer.validated_data['type'],
                                                   scan=serializer.validated_data['scan']).first()
    if previous_scan_photo:
        previous_scan_photo.delete()

    scan_photo = serializer.save()

    updated_serializer = ScanPhotoSerializer(instance=scan_photo)

    return Response({"success": True, "scan_photo": updated_serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_scan_photo(request, scan_photo_id):
    scan_photo = get_object_or_404(ScanPhoto, id=scan_photo_id)

    if scan_photo.scan.user_id != request.user.id:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ScanPhotoSerializer(scan_photo)

    return Response({"scan_photo": serializer.data})


urlpatterns = [
    path("", create_scan_photo),
    path("<int:scan_photo_id>", get_scan_photo)
]
