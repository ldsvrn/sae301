#!/bin/bash

python3 -m venv /home/toto/django/django/sae301/.venv
source /home/toto/django/django/sae301/.venv/bin/activate
pip3 install wheel
pip3 install django django-admin gunicorn paho-mqtt

python3 /home/toto/django/django/sae301/manage.py makemigrations
python3 /home/toto/django/django/sae301/manage.py migrate
python3 /home/toto/django/django/sae301/manage.py collectstatic --noinput