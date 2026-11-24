# CareDesk — Hospital Patient Case Manager

A Django-based starter application for managing inpatient admissions, ward/room/bed assignments, contact details, diagnosis, payment and discharge status.

See `project_report.pdf` for the college-project overview and submission documentation.

## Requirements

- Python 3.12 (the selected version is recorded in `.python-version`)
- Dependencies installed from `requirements.txt`

## Run locally on Windows

From the project directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and sign in using the staff account you created.
Use `/admin/` to manage staff accounts and review records.

## Deploy to Render

Create a **Web Service** for this repository. Configure:

- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn config.wsgi:application`

Gunicorn reads `gunicorn.conf.py` automatically; it binds the service to Render's `PORT` on `0.0.0.0`.

Set these environment variables for the Web Service:

| Variable | Value |
| --- | --- |
| `SECRET_KEY` | A newly generated secret; for example, run `python -c "import secrets; print(secrets.token_urlsafe(50))"` locally and paste its output into Render. |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | The service hostname, such as `your-service.onrender.com` (comma-separate additional hostnames). |
| `DATABASE_URL` | Optional. Set this to a PostgreSQL **Internal Database URL** if using PostgreSQL; when omitted, CareDesk uses SQLite. Keep the URL private. |

Render's `RENDER_EXTERNAL_HOSTNAME` is also added to allowed hosts automatically. The build script installs the requirements, runs Django checks and `collectstatic`, and applies normal migrations with `migrate --noinput` to the configured database. SQLite on Render uses the service's ephemeral filesystem: records may be lost after restarts or redeploys. Login and patient workflows still require an initialized, available database, and this demo does not provide durable storage without PostgreSQL.

After the first successful deployment, open the service's Shell in Render and run:

```sh
python manage.py createsuperuser
```

Use the resulting account to sign in. Patient pages remain login-protected; do not make patient records public.

## Included

- Sign-in required for patient records
- Patient identity and emergency contact information
- Ward, room and bed assignment with duplicate active-bed prevention
- Diagnosis, admission date, doctor, payment type, estimated bill, payment and balance
- Optional insurance and care-team notes
- Search, status filters, case editing and discharge workflow
- Responsive dashboard and case forms

## Demonstration-project safety

CareDesk is a demonstration project, not a system ready for real hospital or clinical use. A Render deployment does not provide the privacy, auditing, backup, access-control, or regulatory safeguards required for real patient records. Do not enter real patient information.
