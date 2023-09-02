FROM python:3.11.5-slim as base
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get -y update && \
    apt-get install -y \
        curl \
        build-essential
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /opt/
WORKDIR /opt
RUN poetry install --only main --no-interaction --no-ansi
ENV PYTHONPATH=/opt
COPY . /opt/

FROM base as dev
RUN poetry install --no-interaction --no-ansi
COPY . /opt/

FROM base as prod
COPY . /opt/
