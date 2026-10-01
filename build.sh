#!/usr/bin/env bash
# Exit on any error so a failed step stops the deploy
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --no-input || true