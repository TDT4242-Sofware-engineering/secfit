#!/usr/bin/env bash
# start.sh
python manage.py migrate

cordova run browser --release --port=3000

gunicorn secfit.wsgi --log-file - -b 0.0.0.0:8000