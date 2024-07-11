#!/bin/sh

cd trueshop
sleep 20
python manage.py makemigrations
python manage.py migrate
gunicorn --workers=2 trueshop.wsgi:application --bind 0.0.0.0:8000