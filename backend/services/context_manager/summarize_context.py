# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Summarize Context
#  File: backend/services/context_manager/summarize_context.py
# ============================================================

from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.chat_messages import ChatMessage
from models.chat_summary import ChatSummary
from integration.llama_client.llama_client import LlamaClient
from core.logging import logger


class SummarizeContext:
    """
    Membuat dan menyimpan ringkasan percakapan ke database.
    Ringkasan dipakai sebagai konteks tambahan untuk AI
    agar tetap ingat topik meski pesan lama sudah tidak dikirim.
    """

    # Buat ringkasan baru setiap kelipatan pesan ini
    SUMMARIZE_EVERY = 10

    def __init__(self, db: AsyncSession):
        self.db = db
        self.llama = LlamaClient()

    async def get_existing_summary(
        self, chat_id: int
    ) -> Optional[ChatSummary]:
        """Ambil ringkasan yang sudah ada dari database."""
        result = await self.db.execute(
            select(ChatSummary).where(ChatSummary.id_chats == chat_id)
        )
        return result.scalar_one_or_none()

    async def should_summarize(
        self, messages: List[ChatMessage]
    ) -> bool:
        """
        Cek apakah perlu membuat ringkasan baru.
        Ringkasan dibuat setiap SUMMARIZE_EVERY pesan.
        """
        return len(messages) > 0 and len(messages) % self.SUMMARIZE_EVERY == 0

    async def create_summary(
        self, chat_id: int, messages: List[ChatMessage]
    ) -> Optional[str]:
        """
        Minta Llama membuat ringkasan dari daftar pesan.
        Simpan atau update ringkasan di database.
        """
        if not messages:
            return None

        # Format pesan menjadi teks untuk dikirim ke AI
        conversation_text = "\n".join([
            f"{msg.role.upper()}: {msg.contents}"
            for msg in messages
        ])

        prompt = (
            "Buatkan ringkasan singkat dari percakapan belajar bahasa Inggris "
            "berikut. Fokus pada topik grammar yang sudah dibahas dan kemajuan "
            f"siswa:\n\n{conversation_text}"
        )

        summary_text, _ = await self.llama.chat(
            context=[],
            user_message=prompt,
        )

        # Simpan atau update di database
        existing = await self.get_existing_summary(chat_id)

        if existing:
            existing.summary_text = summary_text
            await self.db.commit()
        else:
            new_summary = ChatSummary(
                id_chats=chat_id,
                summary_text=summary_text,
            )
            self.db.add(new_summary)
            await self.db.commit()

        logger.info(f"Ringkasan dibuat/diperbarui: chat={chat_id}")
        return summary_text