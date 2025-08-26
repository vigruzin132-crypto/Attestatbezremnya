from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Role
from lessons.models import Lesson, Assignment, Submission
from billing.models import Invoice


@login_required
def dashboard(request):
    user = request.user
    if user.role == Role.ADMIN:
        return render(request, "dashboard_admin.html", {})

    if user.role == Role.TUTOR:
        upcoming_lessons = (
            Lesson.objects.filter(tutor=user).order_by("scheduled_at")[:10]
        )
        recent_assignments = (
            Assignment.objects.filter(assigned_by=user).order_by("-created_at")[:10]
        )
        return render(
            request,
            "dashboard_tutor.html",
            {
                "upcoming_lessons": upcoming_lessons,
                "recent_assignments": recent_assignments,
            },
        )

    if user.role == Role.STUDENT:
        upcoming_lessons = (
            Lesson.objects.filter(student=user).order_by("scheduled_at")[:10]
        )
        my_assignments = Assignment.objects.filter(student=user).order_by("-created_at")[:10]
        my_submissions = Submission.objects.filter(student=user).order_by("-submitted_at")[:10]
        my_invoices = Invoice.objects.filter(student=user).order_by("-issued_at")[:10]
        return render(
            request,
            "dashboard_student.html",
            {
                "upcoming_lessons": upcoming_lessons,
                "my_assignments": my_assignments,
                "my_submissions": my_submissions,
                "my_invoices": my_invoices,
            },
        )

    if user.role == Role.PARENT:
        children = list(user.children.all())
        child_ids = [c.id for c in children]
        invoices = Invoice.objects.filter(student_id__in=child_ids).order_by("-issued_at")[:20]
        upcoming_lessons = Lesson.objects.filter(student_id__in=child_ids).order_by("scheduled_at")[:10]
        return render(
            request,
            "dashboard_parent.html",
            {
                "children": children,
                "invoices": invoices,
                "upcoming_lessons": upcoming_lessons,
            },
        )

    return redirect("login")

# Create your views here.
