#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt
# Convert static asset files
python ./portifolio_server/manage.py collectstatic --no-input
python ./portifolio_server/manage.py createsuperuser

# Apply any outstanding database migrations
python ./portifolio_server/manage.py makemigrations

python ./portifolio_server/manage.py migrate


