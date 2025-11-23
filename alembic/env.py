import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import get_settings
from sqlmodel import SQLModel
from app.models import user, blog, token  # noqa

# Ensure project root is on sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

config = context.config
settings = get_settings()

# Override sqlalchemy.url from our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# We skip logging config to avoid KeyError('formatters')
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
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
