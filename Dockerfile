# syntax=docker/dockerfile:1
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# COPY requirements.txt /app/
# CMD ["/bin/bash","-c","/code/run_cmds.sh"]
# RUN pip install -r requirements.txt

COPY poetry.lock pyproject.toml /app/
RUN pip3 install poetry

COPY . /app/
