#!/usr/bin/env bash
set -eu

python -m pip install -r requirements.txt
python manage.py check
python manage.py collectstatic --noinput
python manage.py migrate --noinput
