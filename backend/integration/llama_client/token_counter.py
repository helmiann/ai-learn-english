# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Token Counter
#  File: backend/integration/llama_client/token_counter.py
# ============================================================

from typing import List, Dict

from core.logging import logger


class TokenCounter:
    """
    Mengestimasi jumlah token sebelum request dikirim ke API.
    Mencegah request yang melebihi batas token model.

    Catatan: Ini adalah estimasi kasar (1 token ≈ 4 karakter).
    Untuk hitungan akurat butuh library tiktoken, tapi itu
    hanya untuk model OpenAI. Untuk Llama, estimasi ini cukup.
    """

    # Estimasi karakter per token
    CHARS_PER_TOKEN = 4

    # Batas token model (sisakan ruang untuk respons)
    MAX_INPUT_TOKENS = 3500

    def estimate_tokens(self, text: str) -> int:
        """Estimasi jumlah token dari satu teks."""
        return max(1, len(text) // self.CHARS_PER_TOKEN)

    def estimate_messages_tokens(
        self, messages: List[Dict[str, str]]
    ) -> int:
        """Estimasi total token dari list messages."""
        total = 0
        for message in messages:
            # Tambah overhead per message (role + formatting)
            total += 4
            total += self.estimate_tokens(message.get("content", ""))
        return total

    def is_within_limit(self, messages: List[Dict[str, str]]) -> bool:
        """
        Cek apakah total token masih dalam batas aman.
        Returns True jika aman, False jika melebihi batas.
        """
        total = self.estimate_messages_tokens(messages)

        if total > self.MAX_INPUT_TOKENS:
            logger.warning(
                f"Token melebihi batas: estimasi={total} "
                f"max={self.MAX_INPUT_TOKENS}"
            )
            return False

        return True

    def get_token_summary(self, messages: List[Dict[str, str]]) -> dict:
        """Ringkasan estimasi token untuk logging."""
        total = self.estimate_messages_tokens(messages)
        return {
            "estimated_tokens": total,
            "max_tokens": self.MAX_INPUT_TOKENS,
            "is_within_limit": total <= self.MAX_INPUT_TOKENS,
            "usage_percent": round((total / self.MAX_INPUT_TOKENS) * 100, 1),
        }