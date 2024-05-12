FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 AS base
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && apt-get -y update \
    && add-apt-repository universe \
    && add-apt-repository ppa:deadsnakes/ppa
RUN apt-get remove -y python3.10
RUN apt-get -y update
RUN apt-get -y install python3.12 \
    python3.12-distutils \
    python3.12-dev \
    python3.12-venv \
    curl \
    && apt-get autoremove -y

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1
RUN update-alternatives --set python3 /usr/bin/python3.12
RUN update-alternatives --set python /usr/bin/python3.12

RUN python -m ensurepip --upgrade \
    && pip3 install --upgrade pip

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

EXPOSE 8080

CMD ["python3", "./app/main.py"]