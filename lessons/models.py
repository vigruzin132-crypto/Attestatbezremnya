from django.db import models
from django.conf import settings
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class LessonStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    COMPLETED = "COMPLETED", "Completed"
    CANCELED = "CANCELED", "Canceled"


class Lesson(models.Model):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="taught_lessons",
        limit_choices_to={"role": "TUTOR"},
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        limit_choices_to={"role": "STUDENT"},
    )
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    status = models.CharField(
        max_length=20, choices=LessonStatus.choices, default=LessonStatus.SCHEDULED
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-scheduled_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.subject} with {self.student} by {self.tutor} on {self.scheduled_at:%Y-%m-%d %H:%M}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments",
        limit_choices_to={"role": "STUDENT"},
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_homework",
        limit_choices_to={"role": "TUTOR"},
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        limit_choices_to={"role": "STUDENT"},
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to="submissions/", blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Submission by {self.student} for {self.assignment}"
