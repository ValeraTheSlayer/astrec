#!/bin/bash
cd /code
poetry install --no-root
#poetry shell
cd project_tracking
poetry run python manage.py runserver 0.0.0.0:8888
