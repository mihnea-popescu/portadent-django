from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import path
from rest_framework.decorators import api_view
from api.serializers import ScanSerializer
from api.models import Scan, ScanStatusType
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


def create_scan(request):
    serializer = ScanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['user_id'] = request.user.id
        serialized_scan = serializer.save()

        scan = Scan.objects.get(id=serialized_scan.id)
        scan.hash = scan.generateHash()
        scan.save()

        # Get the new serializer
        scan_read = ScanSerializer(instance=scan)
        return Response({"scan": scan_read.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_scans(request):
    scan = Scan.objects.filter(user_id=request.user.id).order_by('-id')
    scan_serializer = ScanSerializer(scan, many=True)
    return Response({"scans": scan_serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_scan(request, scan_hash):
    scan = get_object_or_404(Scan, hash=scan_hash, user_id=request.user.id)
    scan_serializer = ScanSerializer(scan)

    if scan.status == ScanStatusType.FINISHED.value and scan.results_viewed == False:
        scan.results_viewed = True
        scan.save()

    return Response({"scan": scan_serializer.data})


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def scan_create_and_read(request):
    if request.method == 'GET':
        return get_scans(request)
    return create_scan(request)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def process_scan(request, scan_id):
    scan = get_object_or_404(Scan, id=scan_id, user_id=request.user.id, status=ScanStatusType.INITIALIZED.value)

    if not scan.hasAllPhotos():
        return Response({"details": "Scan does not have all required photos."}, status=status.HTTP_400_BAD_REQUEST)

    scan.status = ScanStatusType.PHOTOS_FINISHED.value
    scan.save()

    return Response({"success": True})


urlpatterns = [
    path("", scan_create_and_read),
    path("<str:scan_hash>", get_scan),
    path("<int:scan_id>/process/", process_scan)
]
