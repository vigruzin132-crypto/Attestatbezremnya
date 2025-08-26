from django import forms
from django.utils import timezone

from .models import Lesson, Assignment, Submission, Subject


class LessonForm(forms.ModelForm):
    scheduled_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        initial=lambda: timezone.now().replace(second=0, microsecond=0),
    )

    class Meta:
        model = Lesson
        fields = ["subject", "student", "scheduled_at", "duration_minutes", "notes"]


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "lesson", "student", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["assignment", "content", "attachment"]

