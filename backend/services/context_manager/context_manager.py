# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Context Manager (Orkestrator)
#  File: backend/services/context_manager/context_manager.py
# ============================================================

from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from services.context_manager.history_retriever import HistoryRetriever
from services.context_manager.summarize_context import SummarizeContext
from services.context_manager.selection_recent_chat import SelectionRecentChat
from services.context_manager.context_builder import ContextBuilder
from core.logging import logger


class ContextManager:
    """
    Orkestrator utama Context Manager.
    Mengkoordinasikan semua komponen untuk membangun konteks
    yang akan dikirim ke Llama API.

    Alur kerja (sesuai sequence diagram):
    1. HistoryRetriever  — ambil riwayat pesan dari database
    2. SummarizeContext  — buat/ambil ringkasan jika diperlukan
    3. SelectionRecentChat — pilih pesan terbaru yang muat di token limit
    4. ContextBuilder    — rakit semua menjadi konteks final
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.history_retriever = HistoryRetriever(db)
        self.summarize_context = SummarizeContext(db)
        self.selection_recent_chat = SelectionRecentChat()
        self.context_builder = ContextBuilder()

    async def build_context(
        self, chat_id: int
    ) -> List[Dict[str, str]]:
        """
        Bangun konteks lengkap untuk satu sesi chat.
        Dipanggil oleh ChatService sebelum mengirim pesan ke AI.
        """

        # Langkah 1 — Ambil semua riwayat pesan
        all_messages = await self.history_retriever.get_all_messages(chat_id)
        logger.debug(f"Total pesan di history: {len(all_messages)}")

        # Langkah 2 — Buat ringkasan jika sudah waktunya
        summary_text = None
        if await self.summarize_context.should_summarize(all_messages):
            summary_text = await self.summarize_context.create_summary(
                chat_id, all_messages
            )
        else:
            # Ambil ringkasan yang sudah ada sebelumnya
            existing_summary = await self.summarize_context.get_existing_summary(
                chat_id
            )
            if existing_summary:
                summary_text = existing_summary.summary_text

        # Langkah 3 — Pilih pesan terbaru yang muat dalam token limit
        recent_messages = await self.history_retriever.get_recent_messages(
            chat_id
        )
        selected_messages = self.selection_recent_chat.select(recent_messages)

        # Langkah 4 — Rakit konteks final
        context = self.context_builder.build(
            recent_messages=selected_messages,
            summary=summary_text,
        )

        logger.info(
            f"Konteks siap: chat={chat_id} "
            f"pesan={len(selected_messages)} "
            f"ada_summary={summary_text is not None}"
        )

        return context