from __future__ import with_statement

import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context
from app.db.database import Base

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()

config = context.config

# Configurações de logging
fileConfig(config.config_file_name)

# Metadata para autogeração
target_metadata = Base.metadata


# Obter URL do banco de dados a partir da variável de ambiente
def get_url():
    return os.getenv('DATABASE_URL')


def run_migrations_offline():
    """Executa as migrações no modo offline."""
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa as migrações no modo online."""
    connectable = engine_from_config(
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
