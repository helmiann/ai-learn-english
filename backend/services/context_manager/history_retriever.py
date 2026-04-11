# ============================================================
#  ENGLISH GRAMMAR CHATBOT — History Retriever
#  File: backend/services/context_manager/history_retriever.py
# ============================================================

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.chat_messages import ChatMessage
from core.logging import logger


class HistoryRetriever:
    """
    Mengambil riwayat pesan dari database.
    Membatasi jumlah pesan agar tidak melebihi batas token AI.
    """

    # Maksimal pesan yang diambil untuk konteks
    MAX_MESSAGES = 20

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recent_messages(
        self, chat_id: int, limit: int = MAX_MESSAGES
    ) -> List[ChatMessage]:
        """
        Ambil pesan terbaru dari satu sesi chat.
        Diurutkan dari yang paling lama agar urutan percakapan benar.
        """
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.id_chats == chat_id)
            .order_by(ChatMessage.timestamp.desc())
            .limit(limit)
        )
        messages = list(result.scalars().all())

        # Balik urutan: dari lama ke baru
        messages.reverse()

        logger.debug(
            f"History diambil: chat={chat_id} jumlah={len(messages)}"
        )
        return messages

    async def get_all_messages(self, chat_id: int) -> List[ChatMessage]:
        """Ambil semua pesan dalam satu chat (untuk keperluan summary)."""
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.id_chats == chat_id)
            .order_by(ChatMessage.timestamp.asc())
        )
        return list(result.scalars().all())