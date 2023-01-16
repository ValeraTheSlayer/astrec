#!/bin/bash
cd /code
poetry install --no-root
#poetry shell
cd card_approval
poetry run python manage.py runserver 0.0.0.0:8888