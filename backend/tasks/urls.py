from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
    MeAPIView,

    ProjectViewSet,
    CategoryViewSet,
    TagViewSet,
    TaskViewSet,
    GoalViewSet,
    NotificationViewSet,
    CommentViewSet,
    CompanyViewSet,
    UserProfileViewSet,

    DashboardAPIView,
    KanbanAPIView,
    CalendarAPIView,
    StatisticsAPIView,
    EmployeeListAPIView,

    TrashAPIView,
    RestoreTaskAPIView,
    HardDeleteTaskAPIView,

    MoveTaskAPIView,
    ToggleFavoriteAPIView,

    MarkNotificationReadAPIView,
    MarkAllNotificationsReadAPIView,
    UnreadNotificationsAPIView,
)

router = DefaultRouter()

router.register(
    "companies",
    CompanyViewSet,
    basename="companies",
)

router.register(
    "profiles",
    UserProfileViewSet,
    basename="profiles",
)

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
        "me/",
        MeAPIView.as_view(),
        name="me",
    ),

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
    # Employés
    # ==========================

    path(
        "employees/",
        EmployeeListAPIView.as_view(),
        name="employees",
    ),

    # ==========================
    # Corbeille
    # ==========================

    path(
        "trash/",
        TrashAPIView.as_view(),
        name="trash",
    ),

    path(
        "tasks/<int:pk>/restore/",
        RestoreTaskAPIView.as_view(),
        name="restore-task",
    ),

    path(
        "tasks/<int:pk>/hard-delete/",
        HardDeleteTaskAPIView.as_view(),
        name="hard-delete-task",
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
        "notifications/unread/",
        UnreadNotificationsAPIView.as_view(),
        name="notifications-unread",
    ),

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
