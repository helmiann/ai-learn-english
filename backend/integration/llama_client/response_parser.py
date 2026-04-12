# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Response Parser
#  File: backend/integration/llama_client/response_parser.py
# ============================================================

from typing import Tuple

from core.logging import logger


class ResponseParser:
    """
    Mem-parse respons JSON dari Llama API menjadi
    teks dan jumlah token yang mudah dipakai.
    """

    def parse(self, response_data: dict) -> Tuple[str, int]:
        """
        Parse respons dari Llama API.

        Args:
            response_data: Dict hasil response JSON dari API

        Returns:
            Tuple (teks_respons, jumlah_token)
        """
        try:
            # Ambil teks dari choices[0].message.content
            # Format standar OpenAI-compatible API
            choices = response_data.get("choices", [])

            if not choices:
                logger.warning("Response API tidak memiliki choices")
                return "Maaf, saya tidak bisa memproses permintaan ini.", 0

            message = choices[0].get("message", {})
            text = message.get("content", "").strip()

            if not text:
                logger.warning("Response API menghasilkan teks kosong")
                return "Maaf, saya tidak bisa memberikan jawaban saat ini.", 0

            # Ambil jumlah token dari usage
            usage = response_data.get("usage", {})
            token_used = usage.get("total_tokens", 0)

            return text, token_used

        except Exception as e:
            logger.error(f"Error parsing response API: {e}")
            return "Maaf, terjadi kesalahan saat memproses respons.", 0