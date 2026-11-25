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
    is_org_admin,
    is_company_member,
    resolve_space,
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




def _space_queryset(model, request, ordering="-created_at"):

    company, ok = resolve_space(request)

    if not ok:

        return model.objects.none()

    if company is None:

        return model.objects.filter(
            company__isnull=True,
            user=request.user
        ).order_by(ordering)

    return model.objects.filter(
        company=company
    ).order_by(ordering)



def _scoped_tasks(request, include_deleted=False):

    company, ok = resolve_space(request)

    if not ok:

        return Task.objects.none()

    qs = Task.objects.filter(
        is_deleted=include_deleted
    )

    if company is None:

        return qs.filter(
            company__isnull=True,
            user=request.user
        )

    qs = qs.filter(company=company)

    if is_org_admin(request.user, company):

        return qs

    return qs.filter(assigned_to=request.user)


def _get_accessible_task(request, pk, deleted=False):

    from .permissions import task_is_accessible

    try:

        task = Task.objects.get(
            id=pk,
            is_deleted=deleted
        )

    except Task.DoesNotExist:

        return None

    if task_is_accessible(task, request.user):

        return task

    return None

# ============================================================
# ENTREPRISES
# ============================================================


class CompanyViewSet(viewsets.ModelViewSet):

    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return Company.objects.filter(
            Q(owner=user)
            | Q(employees__user=user)
        ).distinct()

    def perform_create(self, serializer):

        company = serializer.save(
            owner=self.request.user
        )

        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user
        )

        profile.company = company
        profile.is_admin = True
        profile.title = (
            self.request.data.get("title")
            or "Administrateur"
        )
        profile.save(
            update_fields=[
                "company",
                "is_admin",
                "title",
            ]
        )

    def get_object(self):

        obj = super().get_object()

        if not is_company_member(
            self.request.user, obj
        ):

            from django.http import Http404

            raise Http404(
                "Organisation introuvable."
            )

        return obj

    def update(self, request, *args, **kwargs):

        company = self.get_object()

        if not is_org_admin(
            request.user, company
        ):

            return Response(
                {"error": "Action réservée aux administrateurs."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(
            request, *args, **kwargs
        )

    def destroy(self, request, *args, **kwargs):

        company = self.get_object()

        if company.owner != request.user:

            return Response(
                {"error": "Seul le propriétaire peut supprimer l'organisation."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(
            request, *args, **kwargs
        )

    @action(detail=False, methods=["post"])
    def join(self, request):

        code = request.data.get("invite_code", "").strip()

        if not code:

            return Response(
                {"error": "Code d'invitation requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            company = Company.objects.get(
                invite_code=code.strip().upper()
            )

        except Company.DoesNotExist:

            return Response(
                {"error": "Code d'invitation invalide."},
                status=status.HTTP_404_NOT_FOUND
            )

        profile, _ = UserProfile.objects.get_or_create(
            user=request.user
        )

        if profile.company_id == company.id:

            return Response(
                {"error": "Vous êtes déjà membre."},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.company = company
        profile.is_admin = False
        profile.title = (
            request.data.get("title") or "Membre"
        )
        profile.save(
            update_fields=[
                "company",
                "is_admin",
                "title",
            ]
        )

        return Response({
            "message": f"Bienvenue dans {company.name} !",
            "company": CompanySerializer(company).data,
        })

    @action(detail=False, methods=["post"])
    def leave(self, request):

        profile = getattr(request.user, "profile", None)

        if not profile or not profile.company:

            return Response(
                {"error": "Aucune organisation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if profile.company.owner == request.user:

            return Response(
                {"error": "Le propriétaire ne peut pas quitter son organisation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.company = None
        profile.is_admin = False
        profile.title = ""
        profile.save(
            update_fields=[
                "company",
                "is_admin",
                "title",
            ]
        )

        return Response({
            "message": "Vous avez quitté l'organisation."
        })

    @action(
        detail=True,
        methods=["post"]
    )
    def regenerate_code(self, request, pk=None):

        company = self.get_object()

        if not is_org_admin(request.user, company):

            return Response(
                {"error": "Action réservée aux administrateurs."},
                status=status.HTTP_403_FORBIDDEN
            )

        company.regenerate_invite_code()

        return Response({
            "invite_code": company.invite_code
        })

    @action(
        detail=True,
        methods=["get", "patch", "post"]
    )
    def members(self, request, pk=None):

        company = self.get_object()

        if request.method == "GET":

            members = UserProfile.objects.filter(
                company=company
            ).select_related("user")

            return Response([
                {
                    "id": m.user.id,
                    "profile_id": m.id,
                    "username": m.user.username,
                    "email": m.user.email,
                    "title": m.title,
                    "is_admin": m.is_admin,
                    "role": m.role,
                    "is_owner": company.owner_id == m.user.id,
                }
                for m in members
            ])

        if not is_org_admin(request.user, company):

            return Response(
                {"error": "Action réservée aux administrateurs."},
                status=status.HTTP_403_FORBIDDEN
            )

        # POST : le responsable crée un compte employé

        if request.method == "POST":

            username = request.data.get("username", "").strip()
            password = request.data.get("password", "")

            if not username or not password:

                return Response(
                    {"error": "Identifiant et mot de passe requis."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if User.objects.filter(
                username=username
            ).exists():

                return Response(
                    {"error": "Cet identifiant existe déjà."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            member_user = User.objects.create_user(
                username=username,
                email=request.data.get("email", ""),
                password=password
            )

            profile = UserProfile.objects.create(
                user=member_user,
                company=company,
                role=UserRole.EMPLOYEE,
                is_admin=bool(
                    request.data.get("is_admin")
                ),
                title=(
                    request.data.get("title")
                    or "Membre"
                )
            )

            return Response({
                "message": f"Compte créé pour {username}.",
                "member": {
                    "id": member_user.id,
                    "profile_id": profile.id,
                    "username": member_user.username,
                    "title": profile.title,
                    "is_admin": profile.is_admin,
                    "is_owner": False,
                },
            }, status=status.HTTP_201_CREATED)

        # PATCH : modification titre / admin

        from django.shortcuts import get_object_or_404

        member = get_object_or_404(
            UserProfile,
            id=request.data.get("profile_id"),
            company=company
        )

        if member.user_id == company.owner_id:

            return Response(
                {"error": "Impossible de modifier le propriétaire."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if "title" in request.data:

            member.title = request.data["title"]

        if "is_admin" in request.data:

            member.is_admin = bool(
                request.data["is_admin"]
            )

        member.save(update_fields=["title", "is_admin"])

        return Response({
            "message": "Membre mis à jour."
        })


# ============================================================
# EMPLOYES
# ============================================================


class EmployeeListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        company, ok = resolve_space(request)

        if not ok or company is None:

            return Response(
                {"error": "Aucune organisation active."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employees = User.objects.filter(
            profile__company=company
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

        return _space_queryset(
            Project,
            self.request,
            "-created_at"
        )

    def perform_create(self, serializer):

        company, _ = resolve_space(self.request)

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

        return _space_queryset(
            Category,
            self.request,
            "name"
        )

    def perform_create(self, serializer):

        company, _ = resolve_space(self.request)

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

        return _space_queryset(
            Tag,
            self.request,
            "name"
        )

    def perform_create(self, serializer):

        company, _ = resolve_space(self.request)

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

        company, ok = resolve_space(self.request)

        if not ok:

            return Task.objects.none()

        if company is None:

            queryset = Task.objects.filter(
                company__isnull=True,
                user=user,
                is_deleted=False
            )

        elif is_org_admin(user, company):

            queryset = Task.objects.filter(
                company=company,
                is_deleted=False
            )

        else:

            queryset = Task.objects.filter(
                company=company,
                assigned_to=user,
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

        # Projet

        project = self.request.query_params.get("project")

        if project:

            queryset = queryset.filter(
                project_id=project
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

        return queryset.order_by(
            "position",
            "-created_at"
        )

    def get_object(self):

        obj = super().get_object()

        from .permissions import task_is_accessible

        if not task_is_accessible(obj, self.request.user):

            from django.http import Http404

            raise Http404("Tâche introuvable.")

        return obj

    def create(self, request, *args, **kwargs):

        _, ok = resolve_space(request)

        if not ok:

            return Response(
                {"error": "Espace inaccessible."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):

        company, _ = resolve_space(self.request)

        task = serializer.save(
            user=self.request.user,
            company=company
        )

        if company is not None:

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

        company, _ = resolve_space(request)

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
        is_admin = False
        title = request.data.get("title", "")

        # Création d'organisation (optionnel)

        if company_name:

            company = Company.objects.create(
                name=company_name,
                description=request.data.get("company_description", ""),
                kind=request.data.get("company_kind", "organization"),
                owner=user
            )

            is_admin = True
            title = title or "Administrateur"

        # Rattachement par code d'invitation (optionnel)

        elif request.data.get("invite_code"):

            try:

                company = Company.objects.get(
                    invite_code=request.data["invite_code"].strip().upper()
                )

            except Company.DoesNotExist:

                return Response(
                    {"error": "Code d'invitation invalide."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = title or "Membre"

        elif company_id:

            try:

                company = Company.objects.get(id=company_id)

            except Company.DoesNotExist:

                return Response(
                    {"error": "Organisation introuvable."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = title or "Membre"

        UserProfile.objects.create(
            user=user,
            company=company,
            role=(
                UserRole.CEO if is_admin
                else UserRole.EMPLOYEE
            ),
            is_admin=is_admin,
            title=title or "Membre"
        )

        return Response(
            {
                "message": "Compte créé avec succès.",
                "user_id": user.id,
                "username": user.username,
                "company_id": company.id if company else None,
            },
            status=status.HTTP_201_CREATED
        )




# ============================================================
# ESPACES UTILISATEUR (/api/me/)
# ============================================================


class MeAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        profile = getattr(user, "profile", None)

        spaces = [{
            "id": "personal",
            "type": "personal",
            "name": "Espace personnel",
            "is_admin": True,
        }]

        company = profile.company if profile else None

        if company:

            spaces.append({
                "id": company.id,
                "type": "organization",
                "name": company.name,
                "kind": company.kind,
                "title": profile.title,
                "is_admin": is_org_admin(user, company),
                "invite_code": (
                    company.invite_code
                    if is_org_admin(user, company)
                    else None
                ),
            })

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "title": profile.title if profile else "",
            "is_admin": (
                is_org_admin(user, company)
                if company else False
            ),
            "company_id": company.id if company else None,
            "spaces": spaces,
        })


# ============================================================
# DASHBOARD API
# ============================================================


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        company, ok = resolve_space(request)

        if not ok:

            return Response(
                {"error": "Espace inaccessible."},
                status=status.HTTP_403_FORBIDDEN
            )

        is_user_ceo = (
            company is None
            or is_org_admin(user, company)
        )

        base_tasks = _scoped_tasks(request)

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
                profile__company=company
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
            "is_admin": is_user_ceo,
            "space": company.name if company else "personal",
            "company": (
                CompanySerializer(company).data
                if company else None
            ),
        })


# ============================================================
# KANBAN API
# ============================================================


class KanbanAPIView(APIView):

    permission_classes = [IsAuthenticated, HasCompanyAccess]

    def get(self, request):

        user = request.user

        _, ok = resolve_space(request)

        if not ok:

            return Response({
                "todo": [],
                "in_progress": [],
                "review": [],
                "done": [],
            })

        tasks = _scoped_tasks(request).filter(
            is_archived=False
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

        task = _get_accessible_task(request, pk)

        if task is None:

            return Response(
                {"error": "Tâche introuvable."},
                status=status.HTTP_404_NOT_FOUND
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

        _, ok = resolve_space(request)

        if not ok:

            return Response([])

        tasks = _scoped_tasks(request).filter(
            is_archived=False,
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

        _, ok = resolve_space(request)

        if not ok:

            return Response({
                "projects": {},
                "tasks": {},
                "priority": {},
                "goals": {},
                "average_progress": 0,
            })

        tasks = _scoped_tasks(request)

        projects = _space_queryset(
            Project, request
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

        tasks = _scoped_tasks(
            request, include_deleted=True
        ).order_by("-deleted_at")

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)


# ============================================================
# RESTAURER UNE TACHE SUPPRIMEE
# ============================================================


class RestoreTaskAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCEOOrTaskAssignee]

    def post(self, request, pk):

        task = _get_accessible_task(
            request, pk, deleted=True
        )

        if task is None:

            return Response(
                {"error": "Tâche introuvable dans la corbeille."},
                status=status.HTTP_404_NOT_FOUND
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

        task = _get_accessible_task(
            request, pk, deleted=True
        )

        if task is None:

            return Response(
                {"error": "Tâche introuvable dans la corbeille."},
                status=status.HTTP_404_NOT_FOUND
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

        task = _get_accessible_task(request, pk)

        if task is None:

            return Response(
                {"error": "Tâche introuvable."},
                status=status.HTTP_404_NOT_FOUND
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
