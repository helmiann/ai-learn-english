# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Logging Configuration
#  File: backend/core/logging.py
# ============================================================

import sys
import os
from loguru import logger

from core.config import settings


def setup_logging() -> None:
    """
    Setup Loguru logger.
    Dipanggil sekali saat aplikasi startup di main.py (lifespan).
    """

    # Hapus handler default loguru
    logger.remove()

    # ----------------------------------------------------------
    # FORMAT LOG
    # ----------------------------------------------------------
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # ----------------------------------------------------------
    # HANDLER 1 — Output ke terminal (console)
    # ----------------------------------------------------------
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=settings.DEBUG,
    )

    # ----------------------------------------------------------
    # HANDLER 2 — Output ke file
    # ----------------------------------------------------------
    # Buat folder logs jika belum ada
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    logger.add(
        settings.LOG_FILE,
        format=log_format,
        level=settings.LOG_LEVEL,
        rotation="10 MB",       # Buat file baru setiap 10 MB
        retention="30 days",    # Hapus log lebih dari 30 hari
        compression="zip",      # Kompres log lama
        backtrace=True,
        diagnose=False,         # Matikan di file (keamanan — jangan log data sensitif)
        encoding="utf-8",
    )

    logger.info(f"Logging aktif | level={settings.LOG_LEVEL} | env={settings.APP_ENV}")


# ----------------------------------------------------------
# Re-export logger agar bisa diimport dari sini
# Penggunaan di file lain:
#   from core.logging import logger
#   logger.info("Pesan log")
#   logger.error("Ada error")
#   logger.warning("Peringatan")
# ----------------------------------------------------------
__all__ = ["logger", "setup_logging"]