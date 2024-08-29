FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

EXPOSE 2000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2000", "--reload"]
