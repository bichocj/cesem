#!/bin/sh

# Collect static files
echo "-------------------------Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "-------------------------Apply database migrations"
python manage.py migrate

# Load migrations
echo "-------------------------Apply loaddata migrations"
python manage.py loaddata users.json
# python manage.py loaddata activities.json

# Start server
# echo "-------------------------Starting server"
# python manage.py runserver 0.0.0.0:8000
gunicorn cesem.wsgi:application --bind 0.0.0.0:8000