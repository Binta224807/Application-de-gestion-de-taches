from rest_framework import serializers

from .models import (
Project,
Category,
Tag,
Task,
Goal,
Notification,
Comment,
)

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

class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
    ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
        ]


class TaskSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(
        read_only=True
    )

    category = CategorySerializer(
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

    is_overdue = serializers.ReadOnlyField()


    class Meta:

        model = Task

        fields = [

            "id",

            "title",

            "description",

            "project",

            "project_id",

            "category",

            "category_id",

            "status",

            "priority",

            "due_date",

            "due_time",

            "estimated_duration",

            "progress",

            "color",

            "is_favorite",

            "is_archived",

            "archive_duration",

            "archived_at",

            "archive_expires_at",

            "completed_at",

            "is_overdue",

            "created_at",

            "updated_at",

        ]


        read_only_fields = [

            "archived_at",

            "archive_expires_at",

            "created_at",

            "updated_at",

        ]

class GoalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]


class NotificationSerializer(serializers.ModelSerializer):


    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
        ]
    

class CommentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]

