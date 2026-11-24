import uuid

from django.core.validators import MinValueValidator
from django.db import models


def new_patient_id():
    return f"PT-{uuid.uuid4().hex[:8].upper()}"


class PatientCase(models.Model):
    class Status(models.TextChoices):
        ADMITTED = "admitted", "Admitted"
        DISCHARGED = "discharged", "Discharged"

    class PaymentType(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        UPI = "upi", "UPI"
        INSURANCE = "insurance", "Insurance"
        OTHER = "other", "Other"

    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"
        OTHER = "other", "Other"
        UNSPECIFIED = "unspecified", "Prefer not to say"

    patient_id = models.CharField(max_length=11, unique=True, default=new_patient_id, editable=False)
    patient_name = models.CharField(max_length=160)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=12, choices=Gender.choices, default=Gender.UNSPECIFIED)
    phone = models.CharField(max_length=24)
    emergency_contact = models.CharField(max_length=160, blank=True)
    emergency_phone = models.CharField(max_length=24, blank=True)
    diagnosis = models.CharField(max_length=240)
    attending_doctor = models.CharField(max_length=160, blank=True)
    ward = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    bed_number = models.CharField(max_length=20)
    admission_date = models.DateField()
    payment_type = models.CharField(max_length=12, choices=PaymentType.choices)
    estimated_bill = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    insurance_provider = models.CharField(max_length=120, blank=True)
    insurance_policy_number = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ADMITTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-admission_date", "-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["ward", "room_number", "bed_number"],
                condition=models.Q(status="admitted"),
                name="unique_occupied_bed",
            )
        ]

    def __str__(self):
        return f"{self.patient_name} ({self.patient_id})"

    @property
    def balance_due(self):
        return max(self.estimated_bill - self.amount_paid, 0)
