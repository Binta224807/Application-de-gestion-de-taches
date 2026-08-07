from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


# ============================================================
# CHOIX
# ============================================================


class Priority(models.TextChoices):

    LOW = "low", "Faible"

    MEDIUM = "medium", "Moyenne"

    HIGH = "high", "Élevée"

    URGENT = "urgent", "Urgente"


class TaskStatus(models.TextChoices):

    TODO = "todo", "À faire"

    IN_PROGRESS = "in_progress", "En cours"

    REVIEW = "review", "À vérifier"

    DONE = "done", "Terminée"


class GoalStatus(models.TextChoices):

    NOT_STARTED = "not_started", "Non commencé"

    IN_PROGRESS = "in_progress", "En cours"

    COMPLETED = "completed", "Terminé"


class NotificationType(models.TextChoices):

    INFO = "info", "Information"

    SUCCESS = "success", "Succès"

    WARNING = "warning", "Avertissement"

    ERROR = "error", "Erreur"


class ArchiveDuration(models.TextChoices):

    SEVEN_DAYS = "7_days", "7 jours"

    FIFTEEN_DAYS = "15_days", "15 jours"

    THIRTY_DAYS = "30_days", "30 jours"


# ============================================================
# PROJET
# ============================================================


class Project(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="projects"

    )

    name = models.CharField(

        max_length=150

    )

    description = models.TextField(

        blank=True

    )

    color = models.CharField(

        max_length=7,

        default="#6366F1"

    )

    icon = models.CharField(

        max_length=30,

        default="📁"

    )

    is_favorite = models.BooleanField(

        default=False

    )

    is_archived = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Projet"

        verbose_name_plural = "Projets"

        constraints = [

            models.UniqueConstraint(

                fields=["user", "name"],

                name="unique_project_name_per_user"

            )

        ]

    def __str__(self):

        return self.name

    @property
    def total_tasks(self):

        return self.tasks.count()

    @property
    def completed_tasks(self):

        return self.tasks.filter(

            status=TaskStatus.DONE

        ).count()

    @property
    def progress(self):

        total = self.total_tasks

        if total == 0:

            return 0

        return round(

            (self.completed_tasks / total) * 100

        )


# ============================================================
# CATEGORIE
# ============================================================


class Category(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="categories"

    )

    name = models.CharField(

        max_length=100

    )

    color = models.CharField(

        max_length=7,

        default="#8B5CF6"

    )

    icon = models.CharField(

        max_length=30,

        default="🏷️"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["name"]

        verbose_name = "Catégorie"

        verbose_name_plural = "Catégories"

        constraints = [

            models.UniqueConstraint(

                fields=["user", "name"],

                name="unique_category_per_user"

            )

        ]

    def __str__(self):

        return self.name


# ============================================================
# TAG
# ============================================================


class Tag(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="tags"

    )

    name = models.CharField(

        max_length=50

    )

    color = models.CharField(

        max_length=7,

        default="#EC4899"

    )

    class Meta:

        ordering = ["name"]

        verbose_name = "Tag"

        verbose_name_plural = "Tags"

        constraints = [

            models.UniqueConstraint(

                fields=["user", "name"],

                name="unique_tag_per_user"

            )

        ]

    def __str__(self):

        return self.name


# ============================================================
# TACHE
# ============================================================


class Task(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="tasks"

    )

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE,

        related_name="tasks",

        blank=True,

        null=True

    )

    category = models.ForeignKey(

        Category,

        on_delete=models.SET_NULL,

        related_name="tasks",

        blank=True,

        null=True

    )

    tags = models.ManyToManyField(

        Tag,

        related_name="tasks",

        blank=True

    )

    title = models.CharField(

        max_length=255

    )

    description = models.TextField(

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=TaskStatus.choices,

        default=TaskStatus.TODO

    )

    priority = models.CharField(

        max_length=20,

        choices=Priority.choices,

        default=Priority.MEDIUM

    )

    start_date = models.DateField(

        blank=True,

        null=True

    )

    due_date = models.DateField(

        blank=True,

        null=True

    )

    due_time = models.TimeField(

        blank=True,

        null=True

    )

    estimated_duration = models.PositiveIntegerField(

        default=0

    )

    progress = models.PositiveIntegerField(

        default=0

    )

    position = models.PositiveIntegerField(

        default=0

    )

    color = models.CharField(

        max_length=7,

        default="#6366F1"

    )

    is_favorite = models.BooleanField(

        default=False

    )

    is_archived = models.BooleanField(

        default=False

    )

    archive_duration = models.CharField(

        max_length=20,

        choices=ArchiveDuration.choices,

        blank=True,

        null=True

    )

    archived_at = models.DateTimeField(

        blank=True,

        null=True

    )

    archive_expires_at = models.DateTimeField(

        blank=True,

        null=True

    )

    ai_summary = models.TextField(

        blank=True

    )

    ai_priority_score = models.FloatField(

        default=0

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    completed_at = models.DateTimeField(

        blank=True,

        null=True

    )

    class Meta:

        ordering = [

            "position",

            "-created_at"

        ]

        verbose_name = "Tâche"

        verbose_name_plural = "Tâches"

    def __str__(self):

        return self.title

    def mark_done(self):

        self.status = TaskStatus.DONE

        self.progress = 100

        self.completed_at = timezone.now()

        self.save()

    def archive(self, duration):

        if duration == ["never","delete"]:

            self.delete()

            return

        days = {

            ArchiveDuration.SEVEN_DAYS: 7,

            ArchiveDuration.FIFTEEN_DAYS: 15,

            ArchiveDuration.THIRTY_DAYS: 30,

        }

        self.is_archived = True

        self.archive_duration = duration

        self.archived_at = timezone.now()

        self.archive_expires_at = (

            timezone.now()

            + timedelta(days=days[duration])

        )

        self.save()

    def restore(self):

        self.is_archived = False

        self.archive_duration = None

        self.archived_at = None

        self.archive_expires_at = None

        self.save()

    @property
    def is_overdue(self):

        if not self.due_date:

            return False

        return (

            self.due_date < timezone.localdate()

            and self.status != TaskStatus.DONE

            and not self.is_archived

        )

    @property
    def project_progress(self):

        if self.project:

            return self.project.progress

        return None


# ============================================================
# OBJECTIFS
# ============================================================


class Goal(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="goals"

    )

    title = models.CharField(

        max_length=255

    )

    description = models.TextField(

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=GoalStatus.choices,

        default=GoalStatus.NOT_STARTED

    )

    progress = models.PositiveIntegerField(

        default=0

    )

    start_date = models.DateField(

        blank=True,

        null=True

    )

    target_date = models.DateField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["target_date"]

        verbose_name = "Objectif"

        verbose_name_plural = "Objectifs"

    def __str__(self):

        return self.title


# ============================================================
# NOTIFICATIONS
# ============================================================


class Notification(models.Model):

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="notifications"

    )

    title = models.CharField(

        max_length=255

    )

    message = models.TextField()

    notification_type = models.CharField(

        max_length=20,

        choices=NotificationType.choices,

        default=NotificationType.INFO

    )

    task = models.ForeignKey(

        Task,

        on_delete=models.CASCADE,

        related_name="notifications",

        blank=True,

        null=True

    )

    is_read = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Notification"

        verbose_name_plural = "Notifications"

    def __str__(self):

        return self.title


# ============================================================
# COMMENTAIRES
# ============================================================


class Comment(models.Model):

    task = models.ForeignKey(

        Task,

        on_delete=models.CASCADE,

        related_name="comments"

    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )

    content = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = ["created_at"]

        verbose_name = "Commentaire"

        verbose_name_plural = "Commentaires"

    def __str__(self):

        return (

            f"{self.user.username} - "

            f"{self.task.title}"

        )