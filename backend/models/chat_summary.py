# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chat Summary Model
#  File: backend/models/chat_summary.py
#  Tabel: chat_summary
# ============================================================

from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ChatSummary(Base):
    __tablename__ = "chat_summary"

    # ----------------------------------------------------------
    # KOLOM
    # ----------------------------------------------------------
    id_chatsummary: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    id_chats: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id_chats", ondelete="CASCADE"),
        nullable=False,
        unique=True,    # Satu chat hanya boleh punya satu summary
        index=True,
    )
    summary_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # ----------------------------------------------------------
    # RELASI
    # ----------------------------------------------------------
    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="summary",
    )

    def __repr__(self) -> str:
        return f"<ChatSummary id={self.id_chatsummary} chat={self.id_chats}>"