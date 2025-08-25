from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TUTOR = "TUTOR", "Tutor"
    STUDENT = "STUDENT", "Student"
    PARENT = "PARENT", "Parent"


class User(AbstractUser):
    """Custom user model with simple role field and parent-child linking.

    Parent-child relationship is represented as an asymmetrical many-to-many
    relation on the same model. Use roles to control which users can be linked
    as parents or children in admin and views.
    """

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        help_text="User role determining available features",
    )

    parents = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="children",
        help_text="Link parent users to this student user",
    )

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    @property
    def is_tutor(self) -> bool:
        return self.role == Role.TUTOR

    @property
    def is_student(self) -> bool:
        return self.role == Role.STUDENT

    @property
    def is_parent(self) -> bool:
        return self.role == Role.PARENT
