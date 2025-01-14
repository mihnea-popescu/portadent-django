from django.shortcuts import redirect
from django.conf import settings


def homepage_redirect_view(request):
    response = redirect(settings.FRONTEND_URL)
    return response
