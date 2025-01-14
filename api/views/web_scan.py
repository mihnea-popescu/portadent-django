from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from api.serializers import WebScanSerializer, FeedbackSerializer
from api.models import User, Scan, ScanSourceType
from rest_framework import status
from django.urls import path
from django.utils import timezone as django_timezone
import random
import string
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.tasks import send_feedback_mail_to_admins, send_registration_email_to_user_with_password


@api_view(['POST'])
def start_scan(request):
    serializer = WebScanSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    email = data['email'].lower()

    if User.objects.filter(email=email).exists():
        return Response({"details": "User already exists!"}, status=status.HTTP_400_BAD_REQUEST)

    # To-Do: Treat the other cases

    # Create User
    user = User.objects.create(email=email, questionnaire_answers=data['questionnaire_answers'])
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    user.username = user.generate_username()
    user.set_password(password)
    user.last_login = django_timezone.now()

    if 'language_tag' in data and data['language_tag']:
        user.language_tag = data['language_tag']

    if 'country_code' in data and data['country_code']:
        user.country_code = data['country_code']

    if 'timezone' in data and data['timezone']:
        user.timezone = data['timezone']

    user.save()

    # Create Scan
    scan = Scan.objects.create(user_id=user.id,
                               source=ScanSourceType.WEB_APP.value)
    scan.hash = scan.generateHash()
    scan.save()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # Send user registration email
    send_registration_email_to_user_with_password.delay(user.id, password)

    return Response({"scan_hash": scan.hash, "access_token": access_token, "refresh_token": refresh_token})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def send_feedback(request):
    serializer = FeedbackSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    send_feedback_mail_to_admins.delay(request.user.id, serializer.validated_data['feedback_type'],
                                       serializer.validated_data['details'], serializer.validated_data['params'])

    return Response({"success": True})


urlpatterns = [
    path('', start_scan),
    path('feedback', send_feedback)
]
