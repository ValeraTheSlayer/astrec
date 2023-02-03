#!/bin/sh
cd /code
poetry install --no-root
#poetry shell
cd arec
poetry run python manage.py runserver 0.0.0.0:8888