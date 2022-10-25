#!/bin/bash

python3 -m venv /home/toto/django/django/.venv
source /home/toto/django/django/.venv/bin/activate
pip3 install django django-admin gunicorn

python3 /home/toto/django/django/manage.py makemigration
python3 /home/toto/django/django/manage.py migrate
python3 /home/toto/django/django/manage.py collectstatic