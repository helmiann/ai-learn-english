# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Error Handler
#  File: backend/integration/llama_client/error_handler.py
# ============================================================

from core.logging import logger


class LlamaAPIError(Exception):
    """Exception khusus untuk error dari Llama API."""

    def __init__(self, message: str, status_code: int = 0):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ErrorHandler:
    """
    Menangani berbagai jenis error dari Llama API
    dan mengubahnya menjadi pesan yang mudah dipahami.
    """

    def handle_http_error(self, status_code: int, response_text: str) -> str:
        """
        Tangani error berdasarkan HTTP status code.

        Returns:
            Pesan error yang ramah untuk ditampilkan ke user
        """
        if status_code == 401:
            logger.error("Llama API: API key tidak valid")
            raise LlamaAPIError("API key tidak valid", status_code)

        elif status_code == 429:
            logger.warning("Llama API: Rate limit tercapai")
            raise LlamaAPIError("Terlalu banyak permintaan, coba lagi sebentar", status_code)

        elif status_code == 400:
            logger.error(f"Llama API: Bad request — {response_text}")
            raise LlamaAPIError("Format permintaan tidak valid", status_code)

        elif status_code == 503:
            logger.error("Llama API: Service tidak tersedia")
            raise LlamaAPIError("Layanan AI sedang tidak tersedia", status_code)

        elif status_code >= 500:
            logger.error(f"Llama API: Server error {status_code}")
            raise LlamaAPIError("Server AI mengalami gangguan", status_code)

        else:
            logger.error(f"Llama API: Error tidak dikenal {status_code} — {response_text}")
            raise LlamaAPIError(f"Error tidak dikenal: {status_code}", status_code)

    def handle_connection_error(self, error: Exception) -> None:
        """Tangani error koneksi ke Llama API."""
        logger.error(f"Llama API: Gagal konek — {error}")
        raise LlamaAPIError("Tidak bisa terhubung ke layanan AI")

    def handle_timeout_error(self) -> None:
        """Tangani error timeout."""
        logger.error("Llama API: Request timeout")
        raise LlamaAPIError("Permintaan ke AI timeout, coba lagi")