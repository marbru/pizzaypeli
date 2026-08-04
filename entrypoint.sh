#!/bin/sh
# This is the entrypoint for the docker container.
# It generates and persists a secret key if one doesn't exists, 
# runs migrations and starts the server.

# Generate secret key if not provided and file doesn't exist
if [ -z "$DJANGO_SECRET_KEY" ]; then
    if [ ! -f /app/data/.secret_key ]; then
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > /app/data/.secret_key
    fi
    export DJANGO_SECRET_KEY=$(cat /app/data/.secret_key)
fi

# Pull the latest imdbinfo on every start (the library frequently needs updates
# to keep up with IMDB's HTML changes). Non-fatal: if PyPI is unreachable, we
# fall back to whatever version is already installed.
pip install -U imdbinfo || echo "Warning: could not update imdbinfo, continuing with installed version"

# Run migrations and start server.
# The "-" log files mean stdout/stderr, so docker captures the access log too.
python manage.py migrate
exec gunicorn --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    pizzaypeli.wsgi:application
