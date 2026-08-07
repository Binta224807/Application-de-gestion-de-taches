from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,

    ProjectViewSet,
    CategoryViewSet,
    TagViewSet,
    TaskViewSet,
    GoalViewSet,
    NotificationViewSet,
    CommentViewSet,

    DashboardAPIView,
    KanbanAPIView,
    CalendarAPIView,
    StatisticsAPIView,

    ArchiveAPIView,
    ArchiveTaskAPIView,
    RestoreTaskAPIView,

    MoveTaskAPIView,
    ToggleFavoriteAPIView,

    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,

    DeleteArchivedTaskAPIView,
)

router = DefaultRouter()

router.register(
    "projects",
    ProjectViewSet,
    basename="projects",
)

router.register(
    "categories",
    CategoryViewSet,
    basename="categories",
)

router.register(
    "tags",
    TagViewSet,
    basename="tags",
)

router.register(
    "tasks",
    TaskViewSet,
    basename="tasks",
)

router.register(
    "goals",
    GoalViewSet,
    basename="goals",
)

router.register(
    "notifications",
    NotificationViewSet,
    basename="notifications",
)

router.register(
    "comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = [

    # ==========================
    # Auth
    # ==========================

    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # ==========================
    # Dashboard
    # ==========================

    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),

    path(
        "kanban/",
        KanbanAPIView.as_view(),
        name="kanban",
    ),

    path(
        "calendar/",
        CalendarAPIView.as_view(),
        name="calendar",
    ),

    path(
        "statistics/",
        StatisticsAPIView.as_view(),
        name="statistics",
    ),

    # ==========================
    # Archives
    # ==========================

    path(
        "archives/",
        ArchiveAPIView.as_view(),
        name="archives",
    ),

    path(
        "tasks/<int:pk>/archive/",
        ArchiveTaskAPIView.as_view(),
        name="archive-task",
    ),

    path(
        "tasks/<int:pk>/restore/",
        RestoreTaskAPIView.as_view(),
        name="restore-task",
    ),

    path(
        "tasks/<int:pk>/delete/",
        DeleteArchivedTaskAPIView.as_view(),
        name="delete-task",
    ),

    # ==========================
    # Kanban
    # ==========================

    path(
        "tasks/<int:pk>/move/",
        MoveTaskAPIView.as_view(),
        name="move-task",
    ),

    path(
        "tasks/<int:pk>/favorite/",
        ToggleFavoriteAPIView.as_view(),
        name="favorite-task",
    ),

    # ==========================
    # Notifications
    # ==========================

    path(
        "notifications/<int:pk>/read/",
        MarkNotificationReadAPIView.as_view(),
        name="notification-read",
    ),

    path(
        "notifications/read-all/",
        MarkAllNotificationsReadAPIView.as_view(),
        name="notifications-read-all",
    ),

    # ==========================
    # CRUD REST Framework
    # ==========================

    path(
        "",
        include(router.urls),
    ),
]