FROM python:3.10.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Ukraine/Kiev
ENV POETRY_HOME=/etc/poetry

RUN apt-get -qqy update && pip install poetry && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app
WORKDIR /app