# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Logger Handler
#  File: backend/infrastructure/logger.py
#
#  File ini menyediakan helper logging tambahan yang spesifik
#  untuk kebutuhan infrastructure seperti mencatat request,
#  response API, dan performa.
# ============================================================

import time
import functools
from typing import Callable, Any

from core.logging import logger


# ----------------------------------------------------------
# DECORATOR — Log waktu eksekusi fungsi
# ----------------------------------------------------------
def log_execution_time(func: Callable) -> Callable:
    """
    Decorator untuk mencatat waktu eksekusi fungsi async.

    Penggunaan:
        @log_execution_time
        async def my_function():
            ...
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.debug(
                f"{func.__name__} selesai dalam {elapsed:.2f}ms"
            )
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            logger.error(
                f"{func.__name__} error setelah {elapsed:.2f}ms: {e}"
            )
            raise
    return wrapper


# ----------------------------------------------------------
# LOG REQUEST — Catat detail request API
# ----------------------------------------------------------
def log_api_request(
    method: str,
    url: str,
    status_code: int,
    duration_ms: float,
) -> None:
    """Catat detail request ke external API (Llama, dll)."""
    level = "info" if status_code < 400 else "error"
    getattr(logger, level)(
        f"API Request | {method} {url} | "
        f"status={status_code} | {duration_ms:.0f}ms"
    )


# ----------------------------------------------------------
# LOG DATABASE — Catat query yang lambat
# ----------------------------------------------------------
def log_slow_query(query: str, duration_ms: float, threshold_ms: float = 500) -> None:
    """Catat query database yang melebihi threshold."""
    if duration_ms > threshold_ms:
        logger.warning(
            f"Slow query ({duration_ms:.0f}ms): {query[:100]}..."
        )


# ----------------------------------------------------------
# LOG CACHE — Catat cache hit/miss
# ----------------------------------------------------------
def log_cache_hit(key: str) -> None:
    logger.debug(f"Cache HIT: {key}")


def log_cache_miss(key: str) -> None:
    logger.debug(f"Cache MISS: {key}")