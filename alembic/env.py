
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

import os
import sys

sys.path.append(os.getcwd())

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

database_url = ''
if os.getenv('APP_SETTINGS') == 'testing':
    database_url = 'sqlite:///' + os.path.join(basedir, 'sqlittest-db.sqlite')
elif os.getenv('APP_SETTINGS') == 'development':
    database_url = 'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite')
elif os.getenv('APP_SETTINGS') == 'production':
    database_url = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config.set_main_option('sqlalchemy.url', database_url)

from api.v2.helpers.database import Base
from api.v2.models.channels.channels_model import Channels
from api.v2.models.bouquets.bouquets_model import Bouquets


target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url").startswith('sqlite:///')
    context.configure(
        url=url, target_metadata=target_metadata, render_as_batch=True,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()