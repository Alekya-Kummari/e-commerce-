#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd e-commerce/ServicesPortal
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
