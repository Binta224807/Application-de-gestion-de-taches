from django.contrib import admin

from .models import (
    Project,
    Category,
    Tag,
    Task,
    Goal,
    Notification,
    Comment,
)


# ============================================================
# PROJECTS
# ============================================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "progress",
        "total_tasks",
        "completed_tasks",
        "is_favorite",
        "is_archived",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_favorite",
        "is_archived",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "user__username",
    )

    readonly_fields = (
        "progress",
        "total_tasks",
        "completed_tasks",
        "created_at",
        "updated_at",
    )


# ============================================================
# CATEGORIES
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "color",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "name",
        "user__username",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# TAGS
# ============================================================

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "color",
    )

    search_fields = (
        "name",
        "user__username",
    )


# ============================================================
# TASKS
# ============================================================

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "project",
        "status",
        "priority",
        "is_favorite",
        "is_archived",
        "archive_duration",
        "archived_at",
        "archive_expires_at",
        "due_date",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "is_favorite",
        "is_archived",
        "archive_duration",
        "due_date",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "user__username",
        "project__name",
    )

    filter_horizontal = (
        "tags",
    )

    readonly_fields = (
        "archived_at",
        "archive_expires_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Informations générales",
            {
                "fields": (
                    "user",
                    "title",
                    "description",
                    "project",
                    "category",
                    "tags",
                )
            }
        ),

        (
            "Organisation",
            {
                "fields": (
                    "status",
                    "priority",
                    "position",
                    "color",
                    "is_favorite",
                )
            }
        ),

        (
            "Dates et durée",
            {
                "fields": (
                    "start_date",
                    "due_date",
                    "due_time",
                    "estimated_duration",
                    "progress",
                )
            }
        ),

        (
            "Archivage",
            {
                "fields": (
                    "is_archived",
                    "archive_duration",
                    "archived_at",
                    "archive_expires_at",
                )
            }
        ),

        (
            "Intelligence artificielle",
            {
                "fields": (
                    "ai_summary",
                    "ai_priority_score",
                )
            }
        ),

        (
            "Dates système",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )


# ============================================================
# GOALS
# ============================================================

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "status",
        "progress",
        "start_date",
        "target_date",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "user__username",
    )

    readonly_fields = (
        "created_at",
    )


# ============================================================
# COMMENTS
# ============================================================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "task",
        "user",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "content",
        "task__title",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )