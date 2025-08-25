from django.contrib import admin

from .models import Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "parent", "amount", "currency", "status", "due_date")
    list_filter = ("status", "currency")
    search_fields = ("id", "student__username", "parent__username")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "paid_at")
    list_filter = ("method",)
    search_fields = ("invoice__id",)

# Register your models here.
