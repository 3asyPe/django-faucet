FROM python:3.11.9

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

ENV PYTHONUNBUFFERED=0
ENV PYTHONDONTWRITEBYTECODE=0
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN poetry install --no-interaction --no-root --no-ansi  --no-cache && \
    apt-get purge --auto-remove -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./src /app/src/

WORKDIR /app
RUN poetry install --only-root
ENV PYTHOPATH=/app/src

COPY ./infra/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN cat /entrypoint.sh

CMD ["/entrypoint.sh"]
