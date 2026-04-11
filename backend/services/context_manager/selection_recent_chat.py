# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Selection Recent Chat
#  File: backend/services/context_manager/selection_recent_chat.py
# ============================================================

from typing import List, Dict

from models.chat_messages import ChatMessage
from core.logging import logger


class SelectionRecentChat:
    """
    Memilih pesan-pesan terbaru yang relevan untuk dikirim ke AI.
    Memastikan jumlah token tidak melebihi batas Llama API.
    """

    # Estimasi batas token untuk pesan (sisakan ruang untuk respons)
    MAX_CONTEXT_TOKENS = 3000
    # Estimasi rata-rata karakter per token
    CHARS_PER_TOKEN = 4

    def select(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """
        Pilih pesan terbaru yang muat dalam batas token.
        Mengembalikan list dict format {"role": ..., "content": ...}
        yang siap dikirim ke Llama API.
        """
        if not messages:
            return []

        selected = []
        total_chars = 0
        max_chars = self.MAX_CONTEXT_TOKENS * self.CHARS_PER_TOKEN

        # Iterasi dari pesan terbaru ke terlama
        for message in reversed(messages):
            msg_chars = len(message.contents)

            if total_chars + msg_chars > max_chars:
                break

            selected.insert(0, {
                "role": message.role,
                "content": message.contents,
            })
            total_chars += msg_chars

        logger.debug(
            f"Pesan dipilih untuk konteks: {len(selected)} "
            f"dari {len(messages)} total"
        )
        return selected