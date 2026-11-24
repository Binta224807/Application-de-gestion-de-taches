from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
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
    Company,
    UserProfile,
    UserRole,
    TaskStatus,
    GoalStatus,
    Priority,
    NotificationType,
)

from .permissions import (
    is_ceo,
    get_user_company,
    IsCEOOrAdmin,
    HasCompanyAccess,
    IsCompanyMember,
    IsTaskAccessible,
    IsCEOOrTaskAssignee,
    IsCompanyOwner,
)

from .serializers import (
    ProjectSerializer,
    CategorySerializer,
    TagSerializer,
    TaskSerializer,
    GoalSerializer,
    NotificationSerializer,
    CommentSerializer,
    CompanySerializer,
    UserProfileSerializer,
    UserSerializer,
)


# ============================================================
# UTILITAIRES
# ============================================================


def create_notification(
    title,
    message,
    recipient,
    notification_type=NotificationType.INFO,
    sender=None,
    task=None,
):

    notification = Notification.objects.create(
        title=title,
        message=message,
        user=recipient,
        sender=sender,
        task=task,
        notification_type=notification_type,
    )

    return notification


def notify_task_assigned(task, recipients=None):

    sender = task.user

    if recipients is None:

        recipients = task.assigned_to.all()

    for recipient in recipients:

        if recipient == sender:

            continue

        create_notification(
            title="Nouvelle tâche assignée",
            message=(
                f"Le PDG vous a assigné une nouvelle tâche : {task.title}."
            ),
            recipient=recipient,
            sender=sender,
            task=task,
            notification_type=NotificationType.INFO,
        )


def notify_status_change(task, previous_status, employee):

    company = task.company

    if not company:

        return

    ceo = company.owner

    if not ceo:

        return

    if task.status == TaskStatus.IN_PROGRESS and previous_status == TaskStatus.TODO:

        create_notification(
            title="Tâche commencée",
            message=(
                f"{employee.username} a commencé la tâche : {task.title}."
            ),
            recipient=ceo,
            sender=employee,
            task=task,
            notification_type=NotificationType.SUCCESS,
        )

    elif task.status == TaskStatus.DONE and previous_status != TaskStatus.DONE:

        create_notification(
            title="Tâche terminée",
            message=(
                f"{employee.username} a terminé la tâche : {task.title}."
            ),
            recipient=ceo,
            sender=employee,
            task=task,
            notification_type=NotificationType.SUCCESS,
        )


# ============================================================
# ENTREPRISES
# ============================================================


class CompanyViewSet(viewsets.ModelViewSet):

    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCEOOrAdmin]

    def get_queryset(self):

        user = self.request.user

        if is_ceo(user):

            return Company.objects.filter(
                owner=user
            )

        return Company.objects.filter(
            employees__user=user
        )

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)


# ============================================================
# EMPLOYES
# ============================================================


class EmployeeListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrAdmin]

    def get(self, request):

        company = get_user_company(request.user)

        if not company:

            return Response(
                {"error": "Aucune entreprise associée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employees = User.objects.filter(
            profile__company=company,
            profile__role=UserRole.EMPLOYEE
        ).select_related("profile")

        serializer = UserSerializer(employees, many=True)

        return Response(serializer.data)


# ============================================================
# PROFILS
# ============================================================


class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return UserProfile.objects.filter(
            user=self.request.user
        )


# ============================================================
# PROJETS
# ============================================================


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get_queryset(self):

        company = get_user_company(self.request.user)

        if not company:

            return Project.objects.none()

        return Project.objects.filter(
            company=company
        ).order_by("-created_at")

    def perform_create(self, serializer):

        company = get_user_company(self.request.user)

        serializer.save(
            user=self.request.user,
            company=company
        )


# ============================================================
# CATEGORIES
# ============================================================


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get_queryset(self):

        company = get_user_company(self.request.user)

        if not company:

            return Category.objects.none()

        return Category.objects.filter(
            company=company
        ).order_by("name")

    def perform_create(self, serializer):

        company = get_user_company(self.request.user)

        serializer.save(
            user=self.request.user,
            company=company
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
    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get_queryset(self):

        company = get_user_company(self.request.user)

        if not company:

            return Tag.objects.none()

        return Tag.objects.filter(
            company=company
        ).order_by("name")

    def perform_create(self, serializer):

        company = get_user_company(self.request.user)

        serializer.save(
            user=self.request.user,
            company=company
        )


# ============================================================
# TASKS
# ============================================================


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get_queryset(self):

        user = self.request.user

        company = get_user_company(user)

        if not company:

            return Task.objects.none()

        queryset = Task.objects.filter(
            company=company,
            is_deleted=False
        )

        # Archives

        archived = self.request.query_params.get("archived", "false")

        if archived.lower() == "true":

            queryset = queryset.filter(
                is_archived=True
            )

        else:

            queryset = queryset.filter(
                is_archived=False
            )

        # Statut

        status_filter = self.request.query_params.get("status")

        if status_filter:

            queryset = queryset.filter(
                status=status_filter
            )

        # Priorité

        priority = self.request.query_params.get("priority")

        if priority:

            queryset = queryset.filter(
                priority=priority
            )

        # Favoris

        favorite = self.request.query_params.get("favorite")

        if favorite == "true":

            queryset = queryset.filter(
                is_favorite=True
            )

        # Employé assigné

        assigned = self.request.query_params.get("assigned")

        if assigned:

            queryset = queryset.filter(
                assigned_to_id=assigned
            )

        # Retard

        overdue = self.request.query_params.get("overdue")

        if overdue == "true":

            queryset = [
                task for task in queryset
                if task.is_overdue
            ]

        # Si employé : seulement ses tâches

        if not is_ceo(user):

            queryset = queryset.filter(
                assigned_to=user
            )

        return queryset.order_by(
            "position",
            "-created_at"
        )

    def get_object(self):

        obj = super().get_object()

        user = self.request.user

        company = get_user_company(user)

        if obj.company != company:

            from django.shortcuts import get_object_or_404
            from django.http import Http404

            raise Http404("Tâche introuvable.")

        if (
            not is_ceo(user)
            and not obj.assigned_to.filter(pk=user.pk).exists()
        ):

            from django.http import Http404

            raise Http404("Tâche introuvable.")

        return obj

    def create(self, request, *args, **kwargs):

        company = get_user_company(request.user)

        if not company:

            return Response(
                {"error": "Aucune entreprise associée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):

        company = get_user_company(self.request.user)

        task = serializer.save(
            user=self.request.user,
            company=company
        )

        notify_task_assigned(task)

    def perform_update(self, serializer):

        task = self.get_object()

        previous_status = task.status

        previous_assigned = set(
            task.assigned_to.values_list("pk", flat=True)
        )

        task = serializer.save()

        # Notification si nouvelle assignation

        new_assignees = task.assigned_to.exclude(
            pk__in=previous_assigned
        ).exclude(
            pk=self.request.user.pk
        )

        notify_task_assigned(task, new_assignees)

        # Notification si changement de statut

        if task.status != previous_status:

            notify_status_change(
                task,
                previous_status,
                self.request.user
            )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):

        task = self.get_object()

        previous_status = task.status

        task.status = TaskStatus.DONE
        task.progress = 100
        task.completed_at = timezone.now()
        task.save()

        notify_status_change(
            task,
            previous_status,
            request.user
        )

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

        company = get_user_company(request.user)

        tasks = Task.objects.filter(
            company=company,
            user=request.user,
            is_archived=True,
            is_deleted=False
        ).order_by("-archived_at")

        serializer = self.get_serializer(tasks, many=True)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        task = self.get_object()

        task.soft_delete()

        return Response(
            {"message": "Tâche déplacée dans la corbeille."},
            status=status.HTTP_200_OK
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
            "message": "Notification marquée comme lue."
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
            "message": f"{updated} notification(s) lue(s)."
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

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")
        email = request.data.get("email", "")
        role = request.data.get("role", UserRole.EMPLOYEE)
        company_name = request.data.get("company_name")
        company_id = request.data.get("company_id")

        if not username or not password:

            return Response(
                {"error": "Username et mot de passe obligatoires."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password_confirmation:

            if password != password_confirmation:

                return Response(
                    {"error": "Les mots de passe ne correspondent pas."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if User.objects.filter(username=username).exists():

            return Response(
                {"error": "Cet utilisateur existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        company = None

        # Création d'entreprise si PDG

        if role == UserRole.CEO and company_name:

            company = Company.objects.create(
                name=company_name,
                description=request.data.get("company_description", ""),
                owner=user
            )

        # Rattachement à une entreprise existante

        elif company_id:

            try:

                company = Company.objects.get(id=company_id)

            except Company.DoesNotExist:

                return Response(
                    {"error": "Entreprise introuvable."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        UserProfile.objects.create(
            user=user,
            company=company,
            role=role
        )

        return Response(
            {
                "message": "Compte créé avec succès.",
                "user_id": user.id,
                "username": user.username,
                "role": role,
                "company_id": company.id if company else None,
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# DASHBOARD API
# ============================================================


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company = get_user_company(user)

        if not company:

            return Response(
                {"error": "Aucune entreprise associée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_user_ceo = is_ceo(user)

        if is_user_ceo:

            base_tasks = Task.objects.filter(
                company=company,
                is_deleted=False
            )

        else:

            base_tasks = Task.objects.filter(
                company=company,
                assigned_to=user,
                is_deleted=False
            )

        active_tasks = base_tasks.filter(
            is_archived=False
        )

        stats = {
            "total_tasks": active_tasks.count(),
            "todo_tasks": active_tasks.filter(
                status=TaskStatus.TODO
            ).count(),
            "in_progress_tasks": active_tasks.filter(
                status=TaskStatus.IN_PROGRESS
            ).count(),
            "review_tasks": active_tasks.filter(
                status=TaskStatus.REVIEW
            ).count(),
            "done_tasks": active_tasks.filter(
                status=TaskStatus.DONE
            ).count(),
            "overdue_tasks": sum(
                1 for task in active_tasks if task.is_overdue
            ),
            "archived_tasks": base_tasks.filter(
                is_archived=True
            ).count(),
            "favorite_tasks": active_tasks.filter(
                is_favorite=True
            ).count(),
            "average_progress": active_tasks.aggregate(
                avg=Avg("progress")
            )["avg"] or 0,
        }

        # Statistiques par employé (PDG uniquement)

        employees_stats = []

        if is_user_ceo:

            employees = User.objects.filter(
                profile__company=company,
                profile__role=UserRole.EMPLOYEE
            )

            for employee in employees:

                emp_tasks = Task.objects.filter(
                    company=company,
                    assigned_to=employee,
                    is_deleted=False,
                    is_archived=False
                )

                employees_stats.append({
                    "id": employee.id,
                    "username": employee.username,
                    "total": emp_tasks.count(),
                    "todo": emp_tasks.filter(
                        status=TaskStatus.TODO
                    ).count(),
                    "in_progress": emp_tasks.filter(
                        status=TaskStatus.IN_PROGRESS
                    ).count(),
                    "done": emp_tasks.filter(
                        status=TaskStatus.DONE
                    ).count(),
                    "overdue": sum(
                        1 for task in emp_tasks if task.is_overdue
                    ),
                })

        recent_tasks = active_tasks.order_by(
            "-updated_at"
        )[:5]

        upcoming_tasks = active_tasks.filter(
            due_date__isnull=False
        ).order_by(
            "due_date"
        )[:5]

        return Response({
            "stats": stats,
            "employees_stats": employees_stats,
            "recent_tasks": TaskSerializer(
                recent_tasks,
                many=True
            ).data,
            "upcoming_tasks": TaskSerializer(
                upcoming_tasks,
                many=True
            ).data,
            "is_ceo": is_user_ceo,
            "company": CompanySerializer(company).data,
        })


# ============================================================
# KANBAN API
# ============================================================


class KanbanAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company = get_user_company(user)

        if not company:

            return Response({
                "todo": [],
                "in_progress": [],
                "review": [],
                "done": [],
            })

        if is_ceo(user):

            tasks = Task.objects.filter(
                company=company,
                is_archived=False,
                is_deleted=False
            )

        else:

            tasks = Task.objects.filter(
                company=company,
                assigned_to=user,
                is_archived=False,
                is_deleted=False
            )

        tasks = tasks.order_by("position")

        return Response({
            "todo": TaskSerializer(
                tasks.filter(status=TaskStatus.TODO),
                many=True
            ).data,
            "in_progress": TaskSerializer(
                tasks.filter(status=TaskStatus.IN_PROGRESS),
                many=True
            ).data,
            "review": TaskSerializer(
                tasks.filter(status=TaskStatus.REVIEW),
                many=True
            ).data,
            "done": TaskSerializer(
                tasks.filter(status=TaskStatus.DONE),
                many=True
            ).data,
        })


# ============================================================
# MOVE TASK (DRAG & DROP)
# ============================================================


class MoveTaskAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrTaskAssignee]

    def post(self, request, pk):

        user = request.user

        company = get_user_company(user)

        try:

            task = Task.objects.get(
                id=pk,
                company=company,
                is_deleted=False
            )

        except Task.DoesNotExist:

            return Response(
                {"error": "Tâche introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            not is_ceo(user)
            and not task.assigned_to.filter(pk=user.pk).exists()
        ):

            return Response(
                {"error": "Accès refusé."},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")
        position = request.data.get("position", 0)

        allowed_status = [
            TaskStatus.TODO,
            TaskStatus.IN_PROGRESS,
            TaskStatus.REVIEW,
            TaskStatus.DONE,
        ]

        if new_status not in allowed_status:

            return Response(
                {"error": "Statut invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        previous_status = task.status

        task.status = new_status
        task.position = position

        if new_status == TaskStatus.DONE:

            task.progress = 100
            task.completed_at = timezone.now()

        else:

            task.completed_at = None

        task.save()

        if task.status != previous_status:

            notify_status_change(
                task,
                previous_status,
                request.user
            )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )


# ============================================================
# CALENDAR API
# ============================================================


class CalendarAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company = get_user_company(user)

        if not company:

            return Response([])

        if is_ceo(user):

            tasks = Task.objects.filter(
                company=company,
                is_archived=False,
                is_deleted=False,
                due_date__isnull=False
            )

        else:

            tasks = Task.objects.filter(
                company=company,
                assigned_to=user,
                is_archived=False,
                is_deleted=False,
                due_date__isnull=False
            )

        tasks = tasks.order_by("due_date")

        events = []

        for task in tasks:

            events.append({
                "id": task.id,
                "title": task.title,
                "date": task.due_date,
                "time": task.due_time,
                "status": task.status,
                "priority": task.priority,
                "color": task.color,
                "project": task.project.name if task.project else None,
                "assigned_to": ", ".join(
                    u.username
                    for u in task.assigned_to.all()
                ),
            })

        return Response(events)


# ============================================================
# STATISTICS API
# ============================================================


class StatisticsAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company = get_user_company(user)

        if not company:

            return Response({
                "projects": {},
                "tasks": {},
                "priority": {},
                "goals": {},
                "average_progress": 0,
            })

        if is_ceo(user):

            tasks = Task.objects.filter(
                company=company,
                is_deleted=False
            )

            projects = Project.objects.filter(
                company=company
            )

        else:

            tasks = Task.objects.filter(
                company=company,
                assigned_to=user,
                is_deleted=False
            )

            projects = Project.objects.filter(
                company=company
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
            avg=Avg("progress")
        )["avg"] or 0

        goals = Goal.objects.filter(
            user=user
        )

        return Response({
            "projects": {
                "total": projects.count(),
                "active": projects.filter(
                    is_archived=False
                ).count(),
                "archived": projects.filter(
                    is_archived=True
                ).count(),
            },
            "tasks": {
                "total": active_tasks.count(),
                "todo": active_tasks.filter(
                    status=TaskStatus.TODO
                ).count(),
                "in_progress": active_tasks.filter(
                    status=TaskStatus.IN_PROGRESS
                ).count(),
                "review": active_tasks.filter(
                    status=TaskStatus.REVIEW
                ).count(),
                "done": completed,
                "archived": archived_tasks.count(),
                "favorites": active_tasks.filter(
                    is_favorite=True
                ).count(),
                "overdue": len(overdue),
            },
            "priority": {
                "low": active_tasks.filter(
                    priority=Priority.LOW
                ).count(),
                "medium": active_tasks.filter(
                    priority=Priority.MEDIUM
                ).count(),
                "high": active_tasks.filter(
                    priority=Priority.HIGH
                ).count(),
                "urgent": active_tasks.filter(
                    priority=Priority.URGENT
                ).count(),
            },
            "goals": {
                "total": goals.count(),
                "completed": goals.filter(
                    status=GoalStatus.COMPLETED
                ).count(),
            },
            "average_progress": round(average_progress),
        })


# ============================================================
# CORBEILLE (TRASH)
# ============================================================


class TrashAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company = get_user_company(user)

        if not company:

            return Response([])

        if is_ceo(user):

            tasks = Task.objects.filter(
                company=company,
                is_deleted=True
            )

        else:

            tasks = Task.objects.filter(
                company=company,
                assigned_to=user,
                is_deleted=True
            )

        tasks = tasks.order_by("-deleted_at")

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)


# ============================================================
# RESTAURER UNE TACHE SUPPRIMEE
# ============================================================


class RestoreTaskAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrTaskAssignee]

    def post(self, request, pk):

        user = request.user

        company = get_user_company(user)

        try:

            task = Task.objects.get(
                id=pk,
                company=company,
                is_deleted=True
            )

        except Task.DoesNotExist:

            return Response(
                {"error": "Tâche introuvable dans la corbeille."},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            not is_ceo(user)
            and not task.assigned_to.filter(pk=user.pk).exists()
        ):

            return Response(
                {"error": "Accès refusé."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.undelete()

        return Response({
            "message": "Tâche restaurée."
        })


# ============================================================
# SUPPRIMER DEFINITIVEMENT UNE TACHE
# ============================================================


class HardDeleteTaskAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrTaskAssignee]

    def delete(self, request, pk):

        user = request.user

        company = get_user_company(user)

        try:

            task = Task.objects.get(
                id=pk,
                company=company,
                is_deleted=True
            )

        except Task.DoesNotExist:

            return Response(
                {"error": "Tâche introuvable dans la corbeille."},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            not is_ceo(user)
            and not task.assigned_to.filter(pk=user.pk).exists()
        ):

            return Response(
                {"error": "Accès refusé."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.delete()

        return Response(
            {"message": "Tâche supprimée définitivement."},
            status=status.HTTP_204_NO_CONTENT
        )


# ============================================================
# TOGGLE FAVORITE
# ============================================================


class ToggleFavoriteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrTaskAssignee]

    def post(self, request, pk):

        user = request.user

        company = get_user_company(user)

        try:

            task = Task.objects.get(
                id=pk,
                company=company,
                is_deleted=False
            )

        except Task.DoesNotExist:

            return Response(
                {"error": "Tâche introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            not is_ceo(user)
            and not task.assigned_to.filter(pk=user.pk).exists()
        ):

            return Response(
                {"error": "Accès refusé."},
                status=status.HTTP_403_FORBIDDEN
            )

        task.is_favorite = not task.is_favorite

        task.save(
            update_fields=["is_favorite"]
        )

        return Response({
            "message": "Favori modifié.",
            "is_favorite": task.is_favorite,
            "task": TaskSerializer(task).data
        })


# ============================================================
# NOTIFICATIONS NON LUES
# ============================================================


class UnreadNotificationsAPIView(APIView):

    permission_classes = [IsAuthenticated]

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

        return Response(serializer.data)


# ============================================================
# MARQUER UNE NOTIFICATION COMME LUE
# ============================================================


class MarkNotificationReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            notification = Notification.objects.get(
                id=pk,
                user=request.user
            )

        except Notification.DoesNotExist:

            return Response(
                {"error": "Notification introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True

        notification.save(
            update_fields=["is_read"]
        )

        return Response({
            "message": "Notification lue."
        })


# ============================================================
# MARQUER TOUTES LES NOTIFICATIONS COMME LUES
# ============================================================


class MarkAllNotificationsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True
        )

        return Response({
            "message": f"{updated} notification(s) lue(s)."
        })
