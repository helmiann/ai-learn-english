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
from schemas.message import MessageResponse
from services.context_manager.context_manager import ContextManager
from integration.llama_client.llama_client import LlamaClient
from core.logging import logger


# ----------------------------------------------------------
# KEYWORD FILTER — Topik di luar 4 materi
# ----------------------------------------------------------
OUT_OF_CONTEXT_KEYWORDS = [
    "future tense", "perfect tense", "continuous tense",
    "passive voice", "conditional", "reported speech",
    "conjunction", "pronoun", "adjective", "adverb",
    "pelajaran berbeda", "bab berbeda", "topik berbeda",
    "bab lain", "pelajaran lain", "ganti pelajaran",
    "selain grammar", "di luar materi",
]

REJECTION_MESSAGE = (
    "Maaf, aku hanya bisa membantu belajar 4 materi grammar SMP:\n\n"
    "1. Simple Present Tense\n"
    "2. Simple Past Tense\n"
    "3. Irregular Verbs\n"
    "4. Imperative Sentences\n\n"
    "Yuk kita fokus pada salah satu materi di atas! "
    "Materi mana yang ingin kamu pelajari? 😊"
)

# ----------------------------------------------------------
# TOPIC KEYWORDS — Deteksi topik dari pesan
# ----------------------------------------------------------
TOPIC_KEYWORDS = {
    "simple_present": [
        "simple present", "present tense", "present simple",
        "kalimat sekarang", "present",
    ],
    "simple_past": [
        "simple past", "past tense", "past simple",
        "kalimat lampau", "kalimat lalu", "waktu lampau",
    ],
    "irregular_verbs": [
        "irregular verb", "irregular verbs", "kata kerja tidak beraturan",
        "verb 2", "verb 3", "bentuk kedua", "bentuk ketiga",
        "irregular", "kata kerja beraturan",
    ],
    "imperative": [
        "imperative", "kalimat perintah", "kalimat larangan",
        "kalimat permintaan", "perintah", "larangan",
    ],
}

TOPIC_SWITCH_MESSAGE = (
    "Sepertinya kamu ingin berpindah ke materi lain. "
    "Untuk menjaga fokus belajar, sebaiknya selesaikan dulu materi "
    "yang sedang kamu pelajari sekarang ya! 😊\n\n"
    "Kalau memang ingin belajar materi lain, kamu bisa:\n"
    "➡️ Buat percakapan baru dari menu sidebar\n\n"
    "Yuk kita lanjutkan belajar di sini dulu! "
    "Ada yang ingin kamu tanyakan tentang materi ini? 💪"
)


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
    # Deteksi topik dari teks pesan
    # ----------------------------------------------------------
    def _detect_topic(self, content: str) -> Optional[str]:
        """Deteksi topik dari sebuah teks pesan."""
        content_lower = content.lower()
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(kw in content_lower for kw in keywords):
                return topic
        return None

    # ----------------------------------------------------------
    # Deteksi topik yang sedang dipelajari di chat ini
    # ----------------------------------------------------------
    async def _get_current_topic(self, chat_id: int) -> Optional[str]:
        """
        Deteksi topik yang sedang dipelajari di chat ini
        berdasarkan pesan-pesan pertama di chat.
        """
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.id_chats == chat_id)
            .order_by(ChatMessage.timestamp.asc())
            .limit(6)  # Cek 6 pesan pertama
        )
        messages = list(result.scalars().all())

        for msg in messages:
            topic = self._detect_topic(msg.contents)
            if topic:
                return topic
        return None

    # ----------------------------------------------------------
    # Cek apakah pesan keluar konteks (di luar 4 materi)
    # ----------------------------------------------------------
    def _is_out_of_context(self, content: str) -> bool:
        content_lower = content.lower()
        return any(
            keyword in content_lower
            for keyword in OUT_OF_CONTEXT_KEYWORDS
        )

    # ----------------------------------------------------------
    # Simpan pesan AI ke database dan return response
    # ----------------------------------------------------------
    async def _save_ai_message(
        self,
        chat_id: int,
        contents: str,
        token_used: int = 0,
    ) -> MessageResponse:
        ai_message = ChatMessage(
            id_chats=chat_id,
            role="assistant",
            contents=contents,
            token_used=token_used,
        )
        self.db.add(ai_message)
        await self.db.commit()
        await self.db.refresh(ai_message)

        return MessageResponse(
            id_chatmassages=ai_message.id_chatmassages,
            id_chats=chat_id,
            role="assistant",
            contents=contents,
            timestamp=ai_message.timestamp,
            token_used=token_used,
        )

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

        # 2. Cek apakah pesan keluar dari 4 materi sama sekali
        if self._is_out_of_context(content):
            logger.info(f"Pesan keluar konteks diblokir: chat={chat_id}")
            return await self._save_ai_message(
                chat_id, REJECTION_MESSAGE
            )

        # 3. Cek apakah siswa minta ganti topik dalam 4 materi
        requested_topic = self._detect_topic(content)
        if requested_topic:
            current_topic = await self._get_current_topic(chat_id)
            if current_topic and current_topic != requested_topic:
                logger.info(
                    f"Ganti topik diblokir: chat={chat_id} "
                    f"current={current_topic} → requested={requested_topic}"
                )
                return await self._save_ai_message(
                    chat_id, TOPIC_SWITCH_MESSAGE
                )

        # 4. Minta context manager siapkan konteks percakapan
        context = await self.context_manager.build_context(chat_id)

        # 5. Kirim ke Llama API dan dapatkan respons
        ai_response_text, token_used = await self.llama.chat(
            context=context,
            user_message=content,
        )

        # 6. Simpan respons AI ke database
        logger.info(f"Pesan diproses: chat={chat_id} token={token_used}")
        return await self._save_ai_message(
            chat_id, ai_response_text, token_used
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
        await self.db.execute(
            delete(ChatMessage).where(ChatMessage.id_chats == chat_id)
        )
        await self.db.execute(
            delete(ChatSummary).where(ChatSummary.id_chats == chat_id)
        )
        await self.db.execute(
            delete(Chat).where(Chat.id_chats == chat_id)
        )
        await self.db.commit()
        logger.info(f"Chat dihapus: id={chat_id}")