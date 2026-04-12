# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Request Formatter
#  File: backend/integration/llama_client/request_formatter.py
# ============================================================

from typing import List, Dict

from core.config import settings


class RequestFormatter:
    """
    Memformat data sebelum dikirim ke Llama API.
    Mengubah list messages menjadi format payload JSON
    yang sesuai dengan standar API Llama.
    """

    def format(
        self,
        context: List[Dict[str, str]],
        user_message: str,
    ) -> dict:
        """
        Buat payload request untuk Llama API.

        Args:
            context : List pesan sebelumnya (dari ContextManager)
            user_message : Pesan terbaru dari siswa

        Returns:
            Dict payload siap dikirim ke API
        """

        # Gabungkan konteks dengan pesan terbaru user
        messages = context.copy()

        # Tambahkan pesan user terbaru jika belum ada di konteks
        if not messages or messages[-1].get("role") != "user":
            messages.append({
                "role": "user",
                "content": user_message,
            })

        payload = {
            "model": settings.LLAMA_MODEL,
            "messages": messages,
            "max_tokens": settings.LLAMA_MAX_TOKENS,
            "temperature": settings.LLAMA_TEMPERATURE,
            "stream": False,
        }

        return payload