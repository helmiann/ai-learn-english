# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Database Connection
#  File: backend/db/database.py
# ============================================================

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from core.config import settings
from core.logging import logger


# ----------------------------------------------------------
# ENGINE — Koneksi utama ke PostgreSQL
# ----------------------------------------------------------
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,        # Print SQL query ke terminal saat DEBUG=true
    pool_size=10,               # Jumlah koneksi yang disimpan di pool
    max_overflow=20,            # Koneksi tambahan saat pool penuh
    pool_pre_ping=True,         # Cek koneksi sebelum dipakai (hindari stale connection)
    pool_recycle=3600,          # Recycle koneksi setiap 1 jam
)


# ----------------------------------------------------------
# SESSION FACTORY
# ----------------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # Objek tetap bisa diakses setelah commit
    autocommit=False,
    autoflush=False,
)


# ----------------------------------------------------------
# INIT DB — Buat semua tabel saat startup
# ----------------------------------------------------------
async def init_db() -> None:
    """
    Buat semua tabel di database berdasarkan model yang sudah didefinisikan.
    Dipanggil saat startup aplikasi di main.py (lifespan).

    Catatan: Di production sebaiknya pakai Alembic migrations,
    bukan create_all. Fungsi ini cocok untuk development.
    """
    # Import semua model agar SQLAlchemy tahu tabel apa yang perlu dibuat
    from models import Base, User, Chat, ChatMessage, ChatSummary, ContextMetadata  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database berhasil diinisialisasi.")


# ----------------------------------------------------------
# DEPENDENCY — Dipakai di route FastAPI
# ----------------------------------------------------------
async def get_db() -> AsyncSession:
    """
    FastAPI dependency untuk mendapatkan sesi database.
    Sesi otomatis ditutup setelah request selesai.

    Penggunaan di route:
        db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ----------------------------------------------------------
# CLOSE DB — Tutup engine saat shutdown
# ----------------------------------------------------------
async def close_db() -> None:
    """
    Tutup semua koneksi database.
    Dipanggil saat shutdown aplikasi di main.py (lifespan).
    """
    await engine.dispose()
    logger.info("Koneksi database ditutup.")