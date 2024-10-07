# Stage 1: Build
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -

ENV PATH=/opt/poetry/bin:${PATH}

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root

# Stage 2: Final
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /opt/poetry /opt/poetry
COPY --from=builder /app /app
COPY . .

ENV PATH=/opt/poetry/bin:${PATH}

RUN poetry install --no-dev --no-root

EXPOSE 2000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2000", "--reload"]
