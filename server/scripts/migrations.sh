#!/bin/bash

/opt/venv/bin/python manage.py makemigrations users
/opt/venv/bin/python manage.py makemigrations gpt
/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate