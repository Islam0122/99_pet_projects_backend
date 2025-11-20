#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate --noinput

python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

exec "$@"
