#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements/production.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
