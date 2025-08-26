from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User, Role
from lessons.models import Subject, Lesson, Assignment
from billing.models import Invoice, InvoiceStatus


class Command(BaseCommand):
    help = "Seed demo data: users, subjects, lessons, assignments, invoices"

    def handle(self, *args, **options):
        # Users
        admin, _ = User.objects.get_or_create(username="admin", defaults={"role": Role.ADMIN, "is_staff": True, "is_superuser": True})
        admin.set_password("admin123"); admin.save()

        tutor, _ = User.objects.get_or_create(username="tutor1", defaults={"role": Role.TUTOR, "email": "tutor@example.com"})
        tutor.set_password("tutor123"); tutor.save()

        parent, _ = User.objects.get_or_create(username="parent1", defaults={"role": Role.PARENT, "email": "parent@example.com"})
        parent.set_password("parent123"); parent.save()

        student, _ = User.objects.get_or_create(username="student1", defaults={"role": Role.STUDENT, "email": "student@example.com"})
        student.set_password("student123"); student.save()

        student.parents.add(parent)

        # Subjects
        math, _ = Subject.objects.get_or_create(name="Математика")
        phys, _ = Subject.objects.get_or_create(name="Физика")

        # Lessons
        l1, _ = Lesson.objects.get_or_create(
            tutor=tutor,
            student=student,
            subject=math,
            scheduled_at=timezone.now() + timezone.timedelta(days=1),
            defaults={"duration_minutes": 60},
        )

        # Assignments
        a1, _ = Assignment.objects.get_or_create(
            title="Домашнее задание #1",
            student=student,
            assigned_by=tutor,
            defaults={"lesson": l1, "description": "Решить задачи 1-5", "due_date": timezone.now().date() + timezone.timedelta(days=7)},
        )

        # Invoices
        inv, _ = Invoice.objects.get_or_create(
            student=student,
            parent=parent,
            amount=3000,
            currency="RUB",
            defaults={"status": InvoiceStatus.SENT, "due_date": timezone.now().date() + timezone.timedelta(days=10)},
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))

