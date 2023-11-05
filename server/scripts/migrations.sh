#!/bin/bash

/opt/venv/bin/python manage.py makemigrations users
/opt/venv/bin/python manage.py makemigrations prompts
/opt/venv/bin/python manage.py makemigrations notekeeper
/opt/venv/bin/python manage.py makemigrations conversations
/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate