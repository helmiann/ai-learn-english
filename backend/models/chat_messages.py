# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chat Messages Model
#  File: backend/models/chat_messages.py
#  Tabel: chat_massages (sesuai ERD)
# ============================================================

from datetime import datetime, timezone

from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_massages"      # Sesuai nama di ERD

    # ----------------------------------------------------------
    # KOLOM
    # ----------------------------------------------------------
    id_chatmassages: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    id_chats: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id_chats", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        # Nilai: "user" atau "assistant"
    )
    contents: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    token_used: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    # ----------------------------------------------------------
    # RELASI
    # ----------------------------------------------------------
    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="messages",
    )

    def __repr__(self) -> str:
        return (
            f"<ChatMessage id={self.id_chatmassages} "
            f"role={self.role} chat={self.id_chats}>"
        )