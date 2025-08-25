from django.shortcuts import render

from accounts.decorators import role_required
from accounts.models import Role
from .models import Invoice


@role_required(Role.STUDENT, Role.PARENT)
def invoice_list(request):
    if request.user.role == Role.STUDENT:
        invoices = Invoice.objects.filter(student=request.user)
    else:
        child_ids = list(request.user.children.values_list("id", flat=True))
        invoices = Invoice.objects.filter(student_id__in=child_ids)
    return render(request, "billing/invoices.html", {"invoices": invoices})

# Create your views here.
