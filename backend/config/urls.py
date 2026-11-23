from django.conf import settings
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import path, include, re_path
from tasks.views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def spa(request):
    """Sert l'application Vue pour toutes les routes hors API."""
    index = settings.REPO_ROOT / "frontend" / "dist" / "index.html"
    if index.exists():
        return FileResponse(index.open("rb"), content_type="text/html")
    raise Http404


urlpatterns = [
    path("admin/", admin.site.urls),

    # API REST
    path("api/", include("tasks.urls")),

    path(
        "api/auth/login/",
        TokenObtainPairView.as_view(),
    ),

    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
    ),
    path(
        "api/auth/register/",
        RegisterView.as_view(),
    ),
    path(
        "api/ai/",
        include("tasks.ai_urls")
    ),


    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),

    # SPA Vue : toutes les autres routes renvoient index.html
    re_path(r"^(?!api/|admin/|static/).*$", spa),
]
