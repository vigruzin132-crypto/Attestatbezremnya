from django.contrib import admin

from .models import Subject, Lesson, Assignment, Submission


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("subject", "tutor", "student", "scheduled_at", "status")
    list_filter = ("status", "subject")
    search_fields = ("tutor__username", "student__username", "subject__name")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "assigned_by", "due_date", "created_at")
    list_filter = ("due_date",)
    search_fields = ("title", "student__username", "assigned_by__username")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "grade")
    list_filter = ("submitted_at",)
    search_fields = ("assignment__title", "student__username")

# Register your models here.
