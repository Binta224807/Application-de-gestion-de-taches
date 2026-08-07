from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Project,
    Category,
    Tag,
    Task,
    Goal,
    Notification,
    Comment,
    TaskStatus,
    GoalStatus,
    Priority,
)

from .serializers import (
    ProjectSerializer,
    CategorySerializer,
    TagSerializer,
    TaskSerializer,
    GoalSerializer,
    NotificationSerializer,
    CommentSerializer,
)
# ============================================================
# PROJECTS
# ============================================================

class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================================================
# CATEGORIES
# ============================================================

class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user
        ).order_by("name")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

# ============================================================
# GOALS
# ============================================================

class GoalViewSet(viewsets.ModelViewSet):

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Goal.objects.filter(
            user=self.request.user
        ).order_by(
            "target_date"
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

# ============================================================
# TAGS
# ============================================================

class TagViewSet(viewsets.ModelViewSet):

    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(
            user=self.request.user
        ).order_by("name")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

# ============================================================
# TASKS
# ============================================================

class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = Task.objects.filter(
            user=self.request.user
        )

        # ==========================
        # Archives
        # ==========================

        archived = self.request.query_params.get("archived", "false")

        if archived.lower() == "true":
            queryset = queryset.filter(
                is_archived=True
            )
        else:
            queryset = queryset.filter(
                is_archived=False
            )

        # ==========================
        # Statut
        # ==========================

        status_filter = self.request.query_params.get("status")

        if status_filter:
            queryset = queryset.filter(
                status=status_filter
            )

        # ==========================
        # Priorité
        # ==========================

        priority = self.request.query_params.get("priority")

        if priority:
            queryset = queryset.filter(
                priority=priority
            )

        # ==========================
        # Favoris
        # ==========================

        favorite = self.request.query_params.get("favorite")

        if favorite == "true":
            queryset = queryset.filter(
                is_favorite=True
            )

        # ==========================
        # Retard
        # ==========================

        overdue = self.request.query_params.get("overdue")

        if overdue == "true":
            queryset = [
                task for task in queryset
                if task.is_overdue
            ]

        return queryset.order_by(
            "position",
            "-created_at"
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        task = self.get_object()

        task.status = TaskStatus.DONE
        task.progress = 100
        task.completed_at = timezone.now()
        task.save()

        return Response({
            "message": "Tâche terminée.",
            "task": TaskSerializer(task).data,
            "ask_archive": True,
        })
    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
            task = self.get_object()

            task.is_favorite = not task.is_favorite
            task.save(update_fields=["is_favorite"])

            return Response(TaskSerializer(task).data)
    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        task = self.get_object()

        duration = request.data.get("duration")

        task.archive(duration)

        return Response({
            "message": "Tâche archivée."
    })
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        task = self.get_object()

        task.restore()

        return Response({
            "message": "Tâche restaurée."
    })
    @action(detail=False, methods=["get"])
    def archived(self, request):
        tasks = Task.objects.filter(
            user=request.user,
            is_archived=True
        ).order_by("-archived_at")

        serializer = self.get_serializer(tasks, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# ============================================================
# NOTIFICATIONS
# ============================================================

class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Notification.objects.filter(
            user=self.request.user
        ).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

    @action(
        detail=True,
        methods=["post"]
    )
    def read(self, request, pk=None):

        notification = self.get_object()

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read"
            ]
        )

        return Response({

            "message":
                "Notification marquée comme lue."

        })

    @action(
        detail=False,
        methods=["post"]
    )
    def read_all(self, request):

        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True
        )

        return Response({

            "message":
                f"{updated} notification(s) lue(s)."

        })

# ============================================================
# COMMENTS
# ============================================================

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Comment.objects.filter(
            user=self.request.user
        ).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

# ============================================================
# REGISTER
# ============================================================

class RegisterView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        username = request.data.get(
            "username"
        )

        password = request.data.get(
            "password"
        )

        password_confirmation = request.data.get(
            "password_confirmation"
        )

        if not username or not password:

            return Response(

                {
                    "error":
                    "Username et mot de passe obligatoires."
                },

                status=status.HTTP_400_BAD_REQUEST

            )

        if password_confirmation:

            if password != password_confirmation:

                return Response(

                    {
                        "error":
                        "Les mots de passe ne correspondent pas."
                    },

                    status=status.HTTP_400_BAD_REQUEST

                )

        if User.objects.filter(
            username=username
        ).exists():

            return Response(

                {
                    "error":
                    "Cet utilisateur existe déjà."
                },

                status=status.HTTP_400_BAD_REQUEST

            )

        user = User.objects.create_user(

            username=username,

            password=password

        )

        return Response(

            {
                "message":
                "Compte créé avec succès.",

                "user_id":
                user.id,

                "username":
                user.username,
            },

            status=status.HTTP_201_CREATED

        )

# ============================================================
# DASHBOARD API
# ============================================================

class DashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        projects = Project.objects.filter(
            user=user,
            is_archived=False
        )

        tasks = Task.objects.filter(
            user=user
        )

        active_tasks = tasks.filter(
            is_archived=False
        )

        goals = Goal.objects.filter(
            user=user
        )

        recent_tasks = active_tasks.order_by(
            "-updated_at"
        )[:5]

        upcoming_tasks = active_tasks.filter(
            due_date__isnull=False
        ).order_by(
            "due_date"
        )[:5]

        stats = {

            "total_projects":
            projects.count(),

            "total_tasks":
            active_tasks.count(),

            "todo_tasks":
            active_tasks.filter(
                status=TaskStatus.TODO
            ).count(),

            "in_progress_tasks":
            active_tasks.filter(
                status=TaskStatus.IN_PROGRESS
            ).count(),

            "review_tasks":
            active_tasks.filter(
                status=TaskStatus.REVIEW
            ).count(),

            "done_tasks":
            active_tasks.filter(
                status=TaskStatus.DONE
            ).count(),

            "archived_tasks":
            tasks.filter(
                is_archived=True
            ).count(),

            "favorite_tasks":
            active_tasks.filter(
                is_favorite=True
            ).count(),

            "average_progress":
            active_tasks.aggregate(
                avg=Avg("progress")
            )["avg"] or 0,

            "total_goals":
            goals.count(),

        }

        projects_progress = []

        for project in projects:

            projects_progress.append({

                "id":
                project.id,

                "name":
                project.name,

                "progress":
                project.progress,

                "completed_tasks":
                project.completed_tasks,

                "total_tasks":
                project.total_tasks,

            })

        return Response({

            "stats":
            stats,

            "projects_progress":
            projects_progress,

            "recent_tasks":
            TaskSerializer(
                recent_tasks,
                many=True
            ).data,

            "upcoming_tasks":
            TaskSerializer(
                upcoming_tasks,
                many=True
            ).data,

            "goals":
            GoalSerializer(
                goals,
                many=True
            ).data,

        })
    

# ============================================================
# KANBAN API
# ============================================================

class KanbanAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        tasks = Task.objects.filter(

            user=request.user,

            is_archived=False

        ).order_by(
            "position"
        )

        return Response({

            "todo":

            TaskSerializer(

                tasks.filter(
                    status=TaskStatus.TODO
                ),

                many=True

            ).data,

            "in_progress":

            TaskSerializer(

                tasks.filter(
                    status=TaskStatus.IN_PROGRESS
                ),

                many=True

            ).data,

            "review":

            TaskSerializer(

                tasks.filter(
                    status=TaskStatus.REVIEW
                ),

                many=True

            ).data,

            "done":

            TaskSerializer(

                tasks.filter(
                    status=TaskStatus.DONE
                ),

                many=True

            ).data,

        })

# ============================================================
# MOVE TASK (DRAG & DROP)
# ============================================================

class MoveTaskAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            task = Task.objects.get(

                id=pk,

                user=request.user

            )

        except Task.DoesNotExist:

            return Response(

                {
                    "error":
                    "Tâche introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        new_status = request.data.get(
            "status"
        )

        position = request.data.get(
            "position",
            0
        )

        allowed_status = [

            TaskStatus.TODO,

            TaskStatus.IN_PROGRESS,

            TaskStatus.REVIEW,

            TaskStatus.DONE,

        ]

        if new_status not in allowed_status:

            return Response(

                {
                    "error":
                    "Statut invalide."
                },

                status=status.HTTP_400_BAD_REQUEST

            )

        task.status = new_status

        task.position = position

        if new_status == TaskStatus.DONE:

            task.progress = 100

            task.completed_at = timezone.now()

        else:

            task.completed_at = None

        task.save()

        return Response(

            TaskSerializer(task).data,

            status=status.HTTP_200_OK

        )

# ============================================================
# CALENDAR API
# ============================================================

class CalendarAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        tasks = Task.objects.filter(

            user=request.user,

            is_archived=False,

            due_date__isnull=False

        ).order_by(
            "due_date"
        )

        events = []

        for task in tasks:

            events.append({

                "id":
                task.id,

                "title":
                task.title,

                "date":
                task.due_date,

                "time":
                task.due_time,

                "status":
                task.status,

                "priority":
                task.priority,

                "color":
                task.color,

                "project":

                task.project.name
                if task.project
                else None

            })

        return Response(events)

# ============================================================
# STATISTICS API
# ============================================================

class StatisticsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        user = request.user

        tasks = Task.objects.filter(
            user=user
        )

        projects = Project.objects.filter(
            user=user
        )

        goals = Goal.objects.filter(
            user=user
        )

        active_tasks = tasks.filter(
            is_archived=False
        )

        archived_tasks = tasks.filter(
            is_archived=True
        )

        completed = active_tasks.filter(

            status=TaskStatus.DONE

        ).count()

        overdue = [

            task.id

            for task in active_tasks

            if task.is_overdue

        ]

        average_progress = active_tasks.aggregate(

            avg=Avg(
                "progress"
            )

        )["avg"] or 0

        return Response({

            "projects": {

                "total":
                projects.count(),

                "active":
                projects.filter(
                    is_archived=False
                ).count(),

                "archived":
                projects.filter(
                    is_archived=True
                ).count(),

            },

            "tasks": {

                "total":
                active_tasks.count(),

                "todo":
                active_tasks.filter(
                    status=TaskStatus.TODO
                ).count(),

                "in_progress":
                active_tasks.filter(
                    status=TaskStatus.IN_PROGRESS
                ).count(),

                "review":
                active_tasks.filter(
                    status=TaskStatus.REVIEW
                ).count(),

                "done":
                completed,

                "archived":
                archived_tasks.count(),

                "favorites":
                active_tasks.filter(
                    is_favorite=True
                ).count(),

                "overdue":
                len(overdue),

            },

            "priority": {

                "low":
                active_tasks.filter(
                    priority=Priority.LOW
                ).count(),

                "medium":
                active_tasks.filter(
                    priority=Priority.MEDIUM
                ).count(),

                "high":
                active_tasks.filter(
                    priority=Priority.HIGH
                ).count(),

                "urgent":
                active_tasks.filter(
                    priority=Priority.URGENT
                ).count(),

            },

            "goals": {

                "total":
                goals.count(),

                "completed":
                goals.filter(
                    status=GoalStatus.COMPLETED
                ).count(),

            },

            "average_progress":
            round(
                average_progress
            ),

        })

# ============================================================
# ARCHIVES
# ============================================================

class ArchiveAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        tasks = Task.objects.filter(

            user=request.user,

            is_archived=True

        ).order_by(
            "-archived_at"
        )

        serializer = TaskSerializer(

            tasks,

            many=True

        )

        return Response(
            serializer.data
        )

# ============================================================
# ARCHIVER UNE TACHE
# ============================================================

class ArchiveTaskAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            task = Task.objects.get(

                id=pk,

                user=request.user

            )

        except Task.DoesNotExist:

            return Response(

                {
                    "error":
                    "Tâche introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        duration = request.data.get(
            "duration"
        )

        task.archive(
            duration
        )

        return Response({

            "message":
            "Tâche archivée."

        })

# ============================================================
# RESTAURER UNE TACHE
# ============================================================

class RestoreTaskAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            task = Task.objects.get(

                id=pk,

                user=request.user

            )

        except Task.DoesNotExist:

            return Response(

                {
                    "error":
                    "Tâche introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        task.restore()

        return Response({

            "message":
            "Tâche restaurée."

        })

# ============================================================
# SUPPRIMER DEFINITIVEMENT UNE ARCHIVE
# ============================================================

class DeleteArchivedTaskAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(self, request, pk):

        try:

            task = Task.objects.get(

                id=pk,

                user=request.user,

                is_archived=True

            )

        except Task.DoesNotExist:

            return Response(

                {
                    "error":
                    "Archive introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        task.delete()

        return Response(

            {
                "message":
                "Archive supprimée définitivement."
            },

            status=status.HTTP_204_NO_CONTENT

        )

# ============================================================
# TOGGLE FAVORITE
# ============================================================

class ToggleFavoriteAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            task = Task.objects.get(

                id=pk,

                user=request.user

            )

        except Task.DoesNotExist:

            return Response(

                {
                    "error":
                    "Tâche introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        task.is_favorite = not task.is_favorite

        task.save(

            update_fields=[
                "is_favorite"
            ]

        )

        return Response({

            "message":

            "Favori modifié.",

            "is_favorite":

            task.is_favorite,

            "task":

            TaskSerializer(task).data

        })

# ============================================================
# NOTIFICATIONS NON LUES
# ============================================================

class UnreadNotificationsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        notifications = Notification.objects.filter(

            user=request.user,

            is_read=False

        ).order_by(

            "-created_at"

        )

        serializer = NotificationSerializer(

            notifications,

            many=True

        )

        return Response(

            serializer.data

        )

# ============================================================
# MARQUER UNE NOTIFICATION COMME LUE
# ============================================================

class MarkNotificationReadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, pk):

        try:

            notification = Notification.objects.get(

                id=pk,

                user=request.user

            )

        except Notification.DoesNotExist:

            return Response(

                {
                    "error":
                    "Notification introuvable."
                },

                status=status.HTTP_404_NOT_FOUND

            )

        notification.is_read = True

        notification.save(

            update_fields=[
                "is_read"
            ]

        )

        return Response({

            "message":
            "Notification lue."

        })

# ============================================================
# MARQUER TOUTES LES NOTIFICATIONS COMME LUES
# ============================================================

class MarkAllNotificationsReadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        updated = Notification.objects.filter(

            user=request.user,

            is_read=False

        ).update(

            is_read=True

        )

        return Response({

            "message":

            f"{updated} notification(s) lue(s)."

        })