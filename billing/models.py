from django.db import models
from django.conf import settings
from django.utils import timezone


class InvoiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SENT = "SENT", "Sent"
    PAID = "PAID", "Paid"
    OVERDUE = "OVERDUE", "Overdue"


class Invoice(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invoices",
        limit_choices_to={"role": "STUDENT"},
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payable_invoices",
        limit_choices_to={"role": "PARENT"},
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=10, default="RUB")
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    issued_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Invoice #{self.id} for {self.student} {self.amount} {self.currency}"

    @property
    def is_overdue(self) -> bool:
        return bool(self.due_date and timezone.now().date() > self.due_date and self.status != InvoiceStatus.PAID)


class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"
    TRANSFER = "TRANSFER", "Bank transfer"


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-paid_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Payment {self.amount} for invoice #{self.invoice_id}"
