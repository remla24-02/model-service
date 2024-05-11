FROM nvcr.io/nvidia/driver:550-5.15.0-1059-oracle-ubuntu22.04 AS base
RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && apt-get -y update \
    && add-apt-repository universe \
    && add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt-get -y install python3.12 \
    python3-pip \
    && apt-get autoremove -y

RUN pip3 install --user --upgrade pip

ENV POETRY_HOME="/opt/poetry"
ENV PYTHONDONTWRITEBYTECODE 1
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base AS install
WORKDIR /home/remla24_team02

ARG INSTALL_ARGS="--no-root"
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
COPY config.ini ./

RUN if [ -f .env ]; then \
    COPY .env .env; \
    fi

RUN addgroup --system --gid 1001 "app-user"
RUN adduser --system --uid 1001 "app-user"
USER "app-user"