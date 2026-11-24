from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PatientCaseForm
from .models import PatientCase


@login_required
def dashboard(request):
    cases = PatientCase.objects.all()
    status = request.GET.get("status", "admitted")
    if status in {PatientCase.Status.ADMITTED, PatientCase.Status.DISCHARGED}:
        cases = cases.filter(status=status)
    else:
        status = "all"

    query = request.GET.get("q", "").strip()
    if query:
        cases = cases.filter(
            Q(patient_name__icontains=query)
            | Q(patient_id__icontains=query)
            | Q(room_number__icontains=query)
            | Q(bed_number__icontains=query)
            | Q(diagnosis__icontains=query)
        )

    billing = PatientCase.objects.filter(status=PatientCase.Status.ADMITTED).aggregate(
        total=Sum("estimated_bill")
    )["total"] or 0
    context = {
        "cases": cases,
        "query": query,
        "status_filter": status,
        "active_count": PatientCase.objects.filter(status=PatientCase.Status.ADMITTED).count(),
        "discharged_count": PatientCase.objects.filter(status=PatientCase.Status.DISCHARGED).count(),
        "billing_total": billing,
    }
    return render(request, "patients/dashboard.html", context)


@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientCaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            messages.success(request, f"Patient case {case.patient_id} was created.")
            return redirect("patient_detail", pk=case.pk)
    else:
        form = PatientCaseForm()
    return render(request, "patients/patient_form.html", {"form": form, "is_edit": False})


@login_required
def patient_detail(request, pk):
    case = get_object_or_404(PatientCase, pk=pk)
    return render(request, "patients/patient_detail.html", {"case": case})


@login_required
def patient_edit(request, pk):
    case = get_object_or_404(PatientCase, pk=pk)
    if request.method == "POST":
        form = PatientCaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient case was updated.")
            return redirect("patient_detail", pk=case.pk)
    else:
        form = PatientCaseForm(instance=case)
    return render(request, "patients/patient_form.html", {"form": form, "is_edit": True, "case": case})


@login_required
@require_POST
def patient_discharge(request, pk):
    case = get_object_or_404(PatientCase, pk=pk)
    if case.status == PatientCase.Status.ADMITTED:
        case.status = PatientCase.Status.DISCHARGED
        case.save(update_fields=["status", "updated_at"])
        messages.success(request, f"{case.patient_name} was marked as discharged.")
    return redirect("patient_detail", pk=case.pk)
