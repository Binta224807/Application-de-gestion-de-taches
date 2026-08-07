from django.contrib import admin
from django.urls import path, include
from tasks.views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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

]