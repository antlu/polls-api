FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=0

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev

RUN adduser -D user

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv \
    && pipenv install --system

USER user

WORKDIR /usr/local/src/polls

COPY . ./

CMD [ "./manage.py", "runserver", "0.0.0.0:8080" ]
