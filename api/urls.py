from django.urls import include, path
from django.views.generic.base import TemplateView
from api.views.core import homepage_redirect_view

urlpatterns = [
    path("auth/", include("api.views.auth")),
    path("user/", include("api.views.user")),
    path("scan/", include("api.views.scan")),
    path("scan-photo/", include("api.views.scan_photo")),
    path("web-scan/", include("api.views.web_scan")),
    path('password-reset/', include("api.views.password_reset")),

    # Other pages
    path("", homepage_redirect_view),
    path("robots.txt", TemplateView.as_view(template_name="core/robots.txt", content_type="text/plain"))
]
