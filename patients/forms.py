from django import forms

from .models import PatientCase


class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = [
            "patient_name",
            "date_of_birth",
            "gender",
            "phone",
            "emergency_contact",
            "emergency_phone",
            "diagnosis",
            "attending_doctor",
            "ward",
            "room_number",
            "bed_number",
            "admission_date",
            "payment_type",
            "estimated_bill",
            "amount_paid",
            "insurance_provider",
            "insurance_policy_number",
            "notes",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        estimated_bill = cleaned_data.get("estimated_bill")
        amount_paid = cleaned_data.get("amount_paid")
        if estimated_bill is not None and amount_paid is not None and amount_paid > estimated_bill:
            self.add_error("amount_paid", "Amount paid cannot exceed the estimated bill.")

        ward = cleaned_data.get("ward")
        room_number = cleaned_data.get("room_number")
        bed_number = cleaned_data.get("bed_number")
        if ward and room_number and bed_number:
            occupied_bed = PatientCase.objects.filter(
                ward=ward,
                room_number=room_number,
                bed_number=bed_number,
                status=PatientCase.Status.ADMITTED,
            )
            if self.instance.pk:
                occupied_bed = occupied_bed.exclude(pk=self.instance.pk)
            if occupied_bed.exists():
                self.add_error("bed_number", "This bed is already assigned to an admitted patient.")
        return cleaned_data
