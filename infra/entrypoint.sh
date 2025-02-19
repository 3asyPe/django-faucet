#!/bin/sh

cd /app/src && poetry run python manage.py migrate
cd /app/src && poetry run gunicorn app.wsgi:application --bind 0.0.0.0:8000
