# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Retry Logic
#  File: backend/integration/llama_client/retry_logic.py
# ============================================================

import asyncio
from typing import Callable, TypeVar, Any

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging

from integration.llama_client.error_handler import LlamaAPIError
from core.logging import logger


T = TypeVar("T")

# Logger standar untuk tenacity
_std_logger = logging.getLogger(__name__)


def create_retry_decorator():
    """
    Buat decorator retry untuk request ke Llama API.

    Strategi:
    - Maksimal 3 percobaan
    - Jeda antar percobaan: 1s, 2s, 4s (exponential backoff)
    - Hanya retry untuk error 429 (rate limit) dan 503 (service unavailable)
    """
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(LlamaAPIError),
        before_sleep=before_sleep_log(_std_logger, logging.WARNING),
        reraise=True,
    )


class RetryLogic:
    """
    Wrapper retry untuk memanggil fungsi async dengan mekanisme retry.
    """

    MAX_ATTEMPTS = 3
    BASE_DELAY = 1.0      # detik
    MAX_DELAY = 10.0      # detik

    async def execute_with_retry(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Jalankan fungsi async dengan retry otomatis.

        Args:
            func    : Fungsi async yang akan dijalankan
            *args   : Argumen posisional untuk func
            **kwargs: Argumen keyword untuk func

        Returns:
            Hasil dari func jika berhasil

        Raises:
            LlamaAPIError jika semua percobaan gagal
        """
        last_error = None
        delay = self.BASE_DELAY

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                return await func(*args, **kwargs)

            except LlamaAPIError as e:
                last_error = e

                # Jangan retry untuk error yang tidak akan berubah
                if e.status_code in (400, 401):
                    logger.error(
                        f"Error tidak bisa di-retry "
                        f"(status={e.status_code}): {e.message}"
                    )
                    raise

                if attempt < self.MAX_ATTEMPTS:
                    logger.warning(
                        f"Percobaan {attempt}/{self.MAX_ATTEMPTS} gagal: "
                        f"{e.message}. Retry dalam {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, self.MAX_DELAY)

            except Exception as e:
                logger.error(f"Error tidak terduga: {e}")
                raise

        logger.error(
            f"Semua {self.MAX_ATTEMPTS} percobaan gagal: {last_error}"
        )
        raise last_error