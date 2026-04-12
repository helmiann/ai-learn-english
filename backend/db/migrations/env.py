# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Alembic Migration Environment
#  File: backend/db/migrations/env.py
# ============================================================

import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ----------------------------------------------------------
# Tambahkan root backend ke sys.path agar bisa import models
# ----------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.config import settings
from models.base import Base

# Import semua model agar Alembic bisa detect perubahan tabel
from models import User, Chat, ChatMessage, ChatSummary, ContextMetadata  # noqa: F401

# ----------------------------------------------------------
# KONFIGURASI ALEMBIC
# ----------------------------------------------------------
config = context.config

# Setup logging dari alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set URL database dari settings (baca dari .env)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Target metadata untuk autogenerate migrations
target_metadata = Base.metadata


# ----------------------------------------------------------
# MIGRASI OFFLINE (tanpa koneksi database)
# ----------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Jalankan migrations tanpa koneksi database aktif.
    Hanya generate SQL script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ----------------------------------------------------------
# MIGRASI ONLINE (dengan koneksi database)
# ----------------------------------------------------------
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,          # Deteksi perubahan tipe kolom
        compare_server_default=True, # Deteksi perubahan default value
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Jalankan migrations secara async."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point untuk migrasi online."""
    asyncio.run(run_async_migrations())


# ----------------------------------------------------------
# JALANKAN
# ----------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()