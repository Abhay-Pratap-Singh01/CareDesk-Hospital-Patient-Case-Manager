from django.contrib import admin

from .models import PatientCase


@admin.register(PatientCase)
class PatientCaseAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id",
        "patient_name",
        "ward",
        "room_number",
        "bed_number",
        "status",
        "admission_date",
    )
    list_filter = ("status", "ward", "payment_type")
    search_fields = ("patient_id", "patient_name", "phone", "diagnosis")
