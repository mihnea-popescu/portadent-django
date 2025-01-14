from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from api.models import User, PasswordReset
from api.serializers import ResetPasswordRequestSerializer, ResetPasswordSerializer
from api.tasks import send_reset_password_email
from django.urls import path
from django.utils import timezone
from datetime import timedelta


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            if user.last_change_password_email_sent_at and user.last_change_password_email_sent_at > timezone.now() - timedelta(
                    minutes=10):
                # sent within the last 5 minutes
                return Response({'success': True}, status=status.HTTP_200_OK)

            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            # Update user last validation email sent at
            user.last_change_password_email_sent_at = timezone.now()
            user.save()

            send_reset_password_email.delay(user.id, token)

        return Response({'success': True}, status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        reset_obj = PasswordReset.objects.filter(token=token, email=data['email']).first()

        if not reset_obj:
            return Response({"details": "Invalid token"},
                            status=status.HTTP_400_BAD_REQUEST)

        if reset_obj.created_at < timezone.now() - timedelta(60):
            return Response({"details": "Expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(data['new_password'])
            user.save()

            reset_obj.delete()

            return Response({'success': True})
        else:
            return Response({'details': 'No user found'}, status=404)


urlpatterns = [
    path('', RequestPasswordReset.as_view()),
    path("<str:token>/", ResetPassword.as_view()),
]
