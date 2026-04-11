# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chat Service
#  File: backend/services/chat_service.py
# ============================================================

from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from models.chats import Chat
from models.chat_messages import ChatMessage
from models.chat_summary import ChatSummary
from schemas.chat import ChatResponse
from schemas.message import MessageResponse
from services.context_manager.context_manager import ContextManager
from integration.llama_client.llama_client import LlamaClient
from core.logging import logger


class ChatService:
    """
    Business logic utama untuk percakapan:
    buat chat, kirim pesan, ambil riwayat, hapus chat.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.llama = LlamaClient()
        self.context_manager = ContextManager(db)

    # ----------------------------------------------------------
    # Buat sesi percakapan baru
    # ----------------------------------------------------------
    async def create_chat(self, user_id: int, title: str) -> Chat:
        chat = Chat(id_user=user_id, title=title)
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    # ----------------------------------------------------------
    # Ambil chat berdasarkan ID
    # ----------------------------------------------------------
    async def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        result = await self.db.execute(
            select(Chat).where(Chat.id_chats == chat_id)
        )
        return result.scalar_one_or_none()

    # ----------------------------------------------------------
    # Ambil semua chat milik satu user
    # ----------------------------------------------------------
    async def get_chats_by_user(self, user_id: int) -> List[Chat]:
        result = await self.db.execute(
            select(Chat)
            .where(Chat.id_user == user_id)
            .order_by(Chat.created_at.desc())
        )
        return list(result.scalars().all())

    # ----------------------------------------------------------
    # Kirim pesan & dapatkan respons AI
    # ----------------------------------------------------------
    async def send_message(
        self,
        chat_id: int,
        user_id: int,
        content: str,
    ) -> MessageResponse:

        # 1. Simpan pesan dari user ke database
        user_message = ChatMessage(
            id_chats=chat_id,
            role="user",
            contents=content,
        )
        self.db.add(user_message)
        await self.db.commit()
        await self.db.refresh(user_message)

        # 2. Minta context manager siapkan konteks percakapan
        context = await self.context_manager.build_context(chat_id)

        # 3. Kirim ke Llama API dan dapatkan respons
        ai_response_text, token_used = await self.llama.chat(
            context=context,
            user_message=content,
        )

        # 4. Simpan respons AI ke database
        ai_message = ChatMessage(
            id_chats=chat_id,
            role="assistant",
            contents=ai_response_text,
            token_used=token_used,
        )
        self.db.add(ai_message)
        await self.db.commit()
        await self.db.refresh(ai_message)

        logger.info(
            f"Pesan diproses: chat={chat_id} token={token_used}"
        )

        return MessageResponse(
            id_chatmassages=ai_message.id_chatmassages,
            id_chats=chat_id,
            role="assistant",
            contents=ai_response_text,
            timestamp=ai_message.timestamp,
            token_used=token_used,
        )

    # ----------------------------------------------------------
    # Ambil semua pesan dalam satu chat
    # ----------------------------------------------------------
    async def get_messages_by_chat(self, chat_id: int) -> List[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.id_chats == chat_id)
            .order_by(ChatMessage.timestamp.asc())
        )
        return list(result.scalars().all())

    # ----------------------------------------------------------
    # Ambil ringkasan chat
    # ----------------------------------------------------------
    async def get_summary_by_chat(
        self, chat_id: int
    ) -> Optional[ChatSummary]:
        result = await self.db.execute(
            select(ChatSummary).where(ChatSummary.id_chats == chat_id)
        )
        return result.scalar_one_or_none()

    # ----------------------------------------------------------
    # Hapus chat beserta semua pesannya
    # ----------------------------------------------------------
    async def delete_chat(self, chat_id: int) -> None:
        # Hapus pesan dulu (foreign key)
        await self.db.execute(
            delete(ChatMessage).where(ChatMessage.id_chats == chat_id)
        )
        # Hapus summary
        await self.db.execute(
            delete(ChatSummary).where(ChatSummary.id_chats == chat_id)
        )
        # Hapus chat
        await self.db.execute(
            delete(Chat).where(Chat.id_chats == chat_id)
        )
        await self.db.commit()
        logger.info(f"Chat dihapus: id={chat_id}")