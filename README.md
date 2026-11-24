# CareDesk — Hospital Patient Case Manager

A Django-based starter application for managing inpatient admissions, ward/room/bed assignments, contact details, diagnosis, payment and discharge status.

See `project_report.pdf` for the college-project overview and submission documentation.

## Requirements

- Python 3.10 or later
- Django (installed from `requirements.txt`)

## Run locally on Windows

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and sign in using the staff account you created.
Use `/admin/` to manage staff accounts and review records.

## Included

- Sign-in required for patient records
- Patient identity and emergency contact information
- Ward, room and bed assignment with duplicate active-bed prevention
- Diagnosis, admission date, doctor, payment type, estimated bill, payment and balance
- Optional insurance and care-team notes
- Search, status filters, case editing and discharge workflow
- Responsive dashboard and case forms

## Before using with real patient information

This is a local development starter, not a production-ready clinical records platform. Before any real deployment, configure a strong `DJANGO_SECRET_KEY`, set `DJANGO_DEBUG=false`, set `DJANGO_ALLOWED_HOSTS`, enable HTTPS, implement backups and access auditing, and have your organization review applicable privacy, security, and medical-record requirements. Do not enter real patient information into an unreviewed development installation.
