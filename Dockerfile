FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false --local && poetry install --no-dev

EXPOSE 8000
