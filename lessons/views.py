from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import Role
from .models import Lesson, Assignment, Submission, Subject
from .forms import LessonForm, AssignmentForm, SubmissionForm


@role_required(Role.TUTOR, Role.STUDENT)
def schedule_view(request):
    if request.user.role == Role.TUTOR:
        lessons = Lesson.objects.filter(tutor=request.user).order_by("scheduled_at")
    else:
        lessons = Lesson.objects.filter(student=request.user).order_by("scheduled_at")
    return render(request, "lessons/schedule.html", {"lessons": lessons})


@role_required(Role.TUTOR)
def lesson_create(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.tutor = request.user
            lesson.save()
            return redirect("schedule")
    else:
        form = LessonForm()
    return render(request, "lessons/lesson_form.html", {"form": form})


@role_required(Role.TUTOR)
def assignment_create(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.assigned_by = request.user
            assignment.save()
            return redirect("dashboard")
    else:
        form = AssignmentForm()
    return render(request, "lessons/assignment_form.html", {"form": form})


@role_required(Role.STUDENT)
def submission_create(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.save()
            return redirect("dashboard")
    else:
        form = SubmissionForm()
    return render(request, "lessons/submission_form.html", {"form": form})

# Create your views here.
