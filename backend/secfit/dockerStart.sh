#!/usr/bin/env bash
# dockerStart.sh
# This file runs at container startup
python manage.py migrate

gunicorn secfit.wsgi --log-file - -b 0.0.0.0:8000