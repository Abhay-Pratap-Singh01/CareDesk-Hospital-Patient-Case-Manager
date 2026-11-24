from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import PatientCase


class PatientCaseWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="staff", password="test-password-123")
        self.client.force_login(self.user)
        self.case_data = {
            "patient_name": "Aarav Sharma",
            "date_of_birth": "1990-04-12",
            "gender": "male",
            "phone": "9876543210",
            "emergency_contact": "Mira Sharma",
            "emergency_phone": "9876543211",
            "diagnosis": "Observation",
            "attending_doctor": "Dr. Rao",
            "ward": "General",
            "room_number": "204",
            "bed_number": "B",
            "admission_date": "2026-11-24",
            "payment_type": "cash",
            "estimated_bill": "12000.00",
            "amount_paid": "5000.00",
            "insurance_provider": "",
            "insurance_policy_number": "",
            "notes": "",
        }

    def test_staff_can_create_patient_case_and_view_balance(self):
        response = self.client.post(reverse("patient_create"), self.case_data)

        self.assertEqual(response.status_code, 302)
        case = PatientCase.objects.get()
        self.assertTrue(case.patient_id.startswith("PT-"))
        self.assertEqual(case.balance_due, Decimal("7000.00"))

    def test_active_bed_cannot_be_assigned_twice(self):
        PatientCase.objects.create(
            patient_name="Existing Patient",
            phone="1234567890",
            diagnosis="Recovery",
            ward="General",
            room_number="204",
            bed_number="B",
            admission_date=date(2026, 11, 23),
            payment_type=PatientCase.PaymentType.CASH,
        )

        response = self.client.post(reverse("patient_create"), self.case_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PatientCase.objects.count(), 1)
        self.assertIn("bed_number", response.context["form"].errors)

    def test_patient_records_require_sign_in(self):
        self.client.logout()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_dashboard_and_patient_detail_render(self):
        case = PatientCase.objects.create(
            patient_name="Aarav Sharma",
            phone="9876543210",
            diagnosis="Observation",
            ward="General",
            room_number="204",
            bed_number="B",
            admission_date=date(2026, 11, 24),
            payment_type=PatientCase.PaymentType.CASH,
        )

        dashboard_response = self.client.get(reverse("dashboard"))
        detail_response = self.client.get(reverse("patient_detail", args=[case.pk]))

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, case.patient_name)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, case.patient_id)
