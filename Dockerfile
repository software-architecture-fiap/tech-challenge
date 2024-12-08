# Stage 1: Build
FROM python:3.10-slim AS builder

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH="/opt/poetry/bin:$PATH"

WORKDIR /app

# Copiar apenas os arquivos necessários
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Stage 2: Final
FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task

# Copiar dependências do estágio de build
COPY --from=builder /usr/local/lib/python3.10/site-packages /var/task/
COPY --from=builder /app /var/task/

# Copiar o código fonte
COPY . .

# Testa o carregamento do driver
RUN python -c "from sqlalchemy.dialects.postgresql import dialect; print('PostgreSQL dialect loaded:', dialect)"

# Configuração do ponto de entrada
CMD ["handler.handler"]
