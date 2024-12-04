from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config
from alembic import context

# Это конфигурация Alembic, взятая из ini-файла.
config = context.config

# Интерпретирует файл конфигурации логирования (если есть).
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импорты моделей для автогенерации схемы
from product_service.app.models import Base  # Замените на путь к вашим моделям

# Добавьте объект `Base` в конфигурацию Alembic.
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Миграции в оффлайн-режиме.
    В этом режиме Alembic генерирует SQL-скрипт вместо выполнения.
    """
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Миграции в онлайн-режиме.
    В этом режиме Alembic выполняет миграции напрямую в базе данных.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection):
    """
    Реальная функция миграции.
    Используется и в онлайн-, и в оффлайн-режимах.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
