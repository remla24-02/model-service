FROM python:3.12.3-slim-bullseye AS base
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y curl \
    && apt-get autoremove -y

ENV POETRY_HOME="/opt/poetry"
ENV PYTHONDONTWRITEBYTECODE 1
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base AS install
WORKDIR /home/remla24_team02

ARG INSTALL_ARGS="--no-root --only main"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="${POETRY_HOME}/bin:$PATH"
COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install $INSTALL_ARGS

RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential \
    && apt-get clean -y \
    && rm -rf /root/.cache \
    && rm -rf /var/apt/lists/* \
    && rm -rf /var/cache/apt/*

FROM install as app-image

ENV PYTHONPATH=/home/remla24_team02/ PYTHONHASHSEED=0

COPY app/ app/
COPY .env config.ini ./

RUN addgroup --system --gid 1001 "app-user"
RUN adduser --system --uid 1001 "app-user"

RUN mkdir -p model && \
    chown -R app-user:app-user model

USER "app-user"

EXPOSE 5001

CMD ["python3", "./app/main.py"]