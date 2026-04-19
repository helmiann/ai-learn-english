# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Redis Client
#  File: backend/infrastructure/redis_client.py
# ============================================================

from typing import Optional, Any
import json

import redis.asyncio as aioredis

from core.config import settings
from core.logging import logger


# ----------------------------------------------------------
# INSTANCE
# ----------------------------------------------------------
_redis: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    """
    Inisialisasi koneksi Redis.
    Dipanggil saat startup aplikasi di main.py (lifespan).
    """
    global _redis

    try:
        _redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=5,
        )
        # Test koneksi
        await _redis.ping()
        logger.info("Redis berhasil terhubung.")
    except Exception as e:
        logger.warning(f"Redis tidak tersedia: {e}. Aplikasi tetap berjalan tanpa cache.")
        _redis = None


async def close_redis() -> None:
    """Tutup koneksi Redis saat shutdown."""
    global _redis
    if _redis:
        await _redis.aclose()
        _redis = None
        logger.info("Koneksi Redis ditutup.")


def get_redis() -> Optional[aioredis.Redis]:
    """Ambil instance Redis. Return None jika tidak tersedia."""
    return _redis


# ----------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------

async def cache_set(key: str, value: Any, expire: int = 3600) -> bool:
    """
    Simpan data ke Redis cache.

    Args:
        key    : Kunci cache
        value  : Data yang disimpan (otomatis di-serialize ke JSON)
        expire : Waktu kedaluwarsa dalam detik (default 1 jam)

    Returns:
        True jika berhasil, False jika Redis tidak tersedia
    """
    if not _redis:
        return False
    try:
        serialized = json.dumps(value, ensure_ascii=False)
        await _redis.set(key, serialized, ex=expire)
        return True
    except Exception as e:
        logger.error(f"Redis set error: {e}")
        return False


async def cache_get(key: str) -> Optional[Any]:
    """
    Ambil data dari Redis cache.

    Returns:
        Data yang tersimpan, atau None jika tidak ada / Redis tidak tersedia
    """
    if not _redis:
        return None
    try:
        data = await _redis.get(key)
        if data is None:
            return None
        return json.loads(data)
    except Exception as e:
        logger.error(f"Redis get error: {e}")
        return None


async def cache_delete(key: str) -> bool:
    """Hapus satu key dari cache."""
    if not _redis:
        return False
    try:
        await _redis.delete(key)
        return True
    except Exception as e:
        logger.error(f"Redis delete error: {e}")
        return False


async def cache_delete_pattern(pattern: str) -> int:
    """
    Hapus semua key yang cocok dengan pattern.
    Contoh: cache_delete_pattern("chat:123:*")

    Returns:
        Jumlah key yang dihapus
    """
    if not _redis:
        return 0
    try:
        keys = await _redis.keys(pattern)
        if keys:
            await _redis.delete(*keys)
        return len(keys)
    except Exception as e:
        logger.error(f"Redis delete pattern error: {e}")
        return 0


# ----------------------------------------------------------
# CACHE KEY HELPERS — Format kunci cache yang konsisten
# ----------------------------------------------------------
def key_chat_messages(chat_id: int) -> str:
    """Key untuk cache pesan dalam satu chat."""
    return f"chat:{chat_id}:messages"


def key_chat_summary(chat_id: int) -> str:
    """Key untuk cache ringkasan chat."""
    return f"chat:{chat_id}:summary"


def key_user_chats(user_id: int) -> str:
    """Key untuk cache daftar chat milik user."""
    return f"user:{user_id}:chats"