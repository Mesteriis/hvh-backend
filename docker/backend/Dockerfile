FROM python:3.12 as base-image

LABEL author="Alexander Mescheryakov <avm@sh-inc.ru>"
LABEL description="Docker image for FastAPI"
LABEL version="1.0.0"
LABEL maintainer="Alexander Mescheryakov <avm@sh-inc.ru>"
LABEL com.sh-inc.vendor="Shade Inc"
LABEL com.sh-inc.label-with-value="Base Image FastAPI"

FROM base-image as install-poetry

ARG POETRY_VERSION="1.8.2"

ENV POETRY_VERSION=${POETRY_VERSION}
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install poetry uvicorn \
    --no-cache-dir --no-color --no-python-version-warning --disable-pip-version-check

FROM install-poetry as install-dependencies

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt
COPY ./backend/pyproject.toml .
COPY ./backend/poetry.lock .
RUN poetry install --no-ansi --no-root --no-dev

FROM install-dependencies as build-image

RUN mkdir -p /app
WORKDIR /app

COPY ./backend/src/* /app

COPY ./docker/backend/start.sh /start
RUN sed -i 's/\r$//g' /start && chmod u+x /start

FROM build-image as final-image

EXPOSE 8000/tcp

CMD ["/start"]
