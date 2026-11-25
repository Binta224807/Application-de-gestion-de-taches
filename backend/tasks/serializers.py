from django.contrib.auth.models import User

from rest_framework import serializers

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
)


# ============================================================
# UTILISATEURS
# ============================================================


class UserProfileSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    class Meta:

        model = UserProfile

        fields = [
            "id",
            "company",
            "company_name",
            "role",
            "title",
            "is_admin",
            "phone",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(
        read_only=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]


# ============================================================
# ENTREPRISES
# ============================================================


class CompanySerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(
        source="owner.username",
        read_only=True
    )

    employee_count = serializers.SerializerMethodField()

    class Meta:

        model = Company

        fields = [
            "id",
            "name",
            "description",
            "kind",
            "invite_code",
            "owner",
            "owner_name",
            "employee_count",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "owner",
            "invite_code",
            "created_at",
            "updated_at",
        ]

    def get_employee_count(self, obj):

        return obj.employees.count()


# ============================================================
# PROJETS
# ============================================================


class ProjectSerializer(serializers.ModelSerializer):

    progress = serializers.ReadOnlyField()
    total_tasks = serializers.ReadOnlyField()
    completed_tasks = serializers.ReadOnlyField()

    class Meta:

        model = Project

        fields = "__all__"

        read_only_fields = [
            "user",
            "progress",
            "total_tasks",
            "completed_tasks",
            "created_at",
            "updated_at",
        ]


# ============================================================
# CATEGORIES
# ============================================================


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = "__all__"

        read_only_fields = [
            "user",
            "created_at",
        ]


# ============================================================
# TAGS
# ============================================================


class TagSerializer(serializers.ModelSerializer):

    class Meta:

        model = Tag

        fields = "__all__"

        read_only_fields = [
            "user",
            "created_at",
        ]


# ============================================================
# TACHES
# ============================================================


class TaskSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(
        read_only=True
    )

    category = CategorySerializer(
        read_only=True
    )

    company = CompanySerializer(
        read_only=True
    )

    created_by = serializers.CharField(
        source="user.username",
        read_only=True
    )

    assigned_to = UserSerializer(
        many=True,
        read_only=True
    )

    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="project",
        write_only=True,
        required=False,
        allow_null=True
    )

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True
    )

    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assigned_to",
        write_only=True,
        many=True,
        required=False
    )

    is_overdue = serializers.ReadOnlyField()

    duration_display = serializers.SerializerMethodField()

    class Meta:

        model = Task

        fields = [
            "id",
            "title",
            "description",
            "user",
            "created_by",
            "company",
            "assigned_to",
            "assigned_to_ids",
            "project",
            "project_id",
            "category",
            "category_id",
            "tags",
            "status",
            "priority",
            "start_date",
            "due_date",
            "due_time",
            "estimated_duration",
            "duration_display",
            "progress",
            "position",
            "color",
            "is_favorite",
            "is_archived",
            "archive_duration",
            "archived_at",
            "archive_expires_at",
            "completed_at",
            "is_deleted",
            "deleted_at",
            "is_overdue",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "archived_at",
            "archive_expires_at",
            "completed_at",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):

        request = self.context.get("request")

        if not (request and request.user):

            return data

        company = (
            self.instance.company
            if self.instance is not None
            else None
        )

        if company is None:

            from .permissions import resolve_space

            company, _ = resolve_space(request)

        assigned_to = data.get("assigned_to")

        if company is None:

            if assigned_to:

                for assignee in assigned_to:

                    if assignee != request.user:

                        raise serializers.ValidationError(
                            "Une tâche personnelle ne peut être assignée qu'à vous-même."
                        )

            project = data.get("project")

            if project and (
                project.company is not None
                or project.user != request.user
            ):

                raise serializers.ValidationError(
                    "Le projet doit appartenir à votre espace personnel."
                )

            category = data.get("category")

            if category and (
                category.company is not None
                or category.user != request.user
            ):

                raise serializers.ValidationError(
                    "La catégorie doit appartenir à votre espace personnel."
                )

            return data

        if assigned_to:

            for assignee in assigned_to:

                from .permissions import is_company_member

                if not is_company_member(
                    assignee, company
                ):

                    raise serializers.ValidationError(
                        "Les membres assignés doivent appartenir à la même organisation."
                    )

        project = data.get("project")

        if project and project.company != company:

            raise serializers.ValidationError(
                "Le projet doit appartenir à la même organisation."
            )

        category = data.get("category")

        if category and category.company != company:

            raise serializers.ValidationError(
                "La catégorie doit appartenir à la même organisation."
            )

        return data

    def get_duration_display(self, obj):

        minutes = obj.estimated_duration

        if minutes < 60:

            return f"{minutes} min"

        hours = minutes // 60

        remaining = minutes % 60

        if remaining == 0:

            return f"{hours} h"

        return f"{hours} h {remaining}"


# ============================================================
# OBJECTIFS
# ============================================================


class GoalSerializer(serializers.ModelSerializer):

    class Meta:

        model = Goal

        fields = "__all__"

        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]


# ============================================================
# NOTIFICATIONS
# ============================================================


class NotificationSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.username",
        read_only=True
    )

    task_title = serializers.CharField(
        source="task.title",
        read_only=True
    )

    class Meta:

        model = Notification

        fields = [
            "id",
            "title",
            "message",
            "sender",
            "sender_name",
            "user",
            "task",
            "task_title",
            "notification_type",
            "is_read",
            "created_at",
        ]

        read_only_fields = [
            "sender",
            "user",
            "task",
            "created_at",
        ]


# ============================================================
# COMMENTAIRES
# ============================================================


class CommentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comment

        fields = "__all__"

        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]
