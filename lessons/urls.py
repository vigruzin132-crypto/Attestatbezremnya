from django.urls import path

from . import views


urlpatterns = [
    path("schedule/", views.schedule_view, name="schedule"),
    path("lessons/create/", views.lesson_create, name="lesson_create"),
    path("assignments/create/", views.assignment_create, name="assignment_create"),
    path("submissions/create/", views.submission_create, name="submission_create"),
]

