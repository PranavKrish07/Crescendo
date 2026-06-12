#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
poetry install

python manage.py collectstatic --no-input

python manage.py migrate

python seed_roadmaps.py