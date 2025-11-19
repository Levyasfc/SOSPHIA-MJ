from __future__ import with_statement
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ⬇️ Cargar variables de entorno (.env)
from dotenv import load_dotenv
load_dotenv()

# Alembic config
config = context.config

# ⬇️ Obtener DATABASE_URL desde entorno
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise Exception("DATABASE_URL no está definida en el entorno")

# ⬇️ Sobrescribir sqlalchemy.url de alembic.ini
config.set_main_option("sqlalchemy.url", database_url)

# Log config
fileConfig(config.config_file_name)

# ⬇️ Importar Base desde el archivo correcto
from app.database import Base

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
