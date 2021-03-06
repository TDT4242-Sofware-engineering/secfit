#!/usr/bin/env bash
# start.sh
python manage.py migrate

gunicorn secfit.wsgi --log-file - -b 0.0.0.0:8000