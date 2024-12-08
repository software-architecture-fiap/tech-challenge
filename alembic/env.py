from __future__ import with_statement

import os
import sys
from pathlib import Path
from logging.config import fileConfig
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Engine
from alembic import context

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.database import Base

load_dotenv()
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_url() -> Optional[str]:
    """Obter URL do banco de dados a partir da variável de ambiente.

    Returns:
        Optional[str]: A URL do banco de dados, se definida.
    """
    return os.getenv('DATABASE_URL')


def run_migrations_offline() -> None:
    """Executa as migrações no modo offline.

    A URL do banco de dados é obtida e usada para configurar o contexto de migração.
    As migrações são então executadas sem necessidade de conexão ativa com o banco de dados.
    """
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo online.

    Um engine é criado e usado para conectar ao banco de dados. As migrações
    são executadas dentro de uma transação ativa.
    """
    connectable: Engine = engine_from_config(
        config.get_section(config.config_ini_section), prefix='sqlalchemy.', poolclass=pool.NullPool, url=get_url()
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
