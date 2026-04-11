# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chats Model
#  File: backend/models/chats.py
#  Tabel: chats
# ============================================================

from datetime import datetime, timezone

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    # ----------------------------------------------------------
    # KOLOM
    # ----------------------------------------------------------
    id_chats: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id_user", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Percakapan Baru",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # ----------------------------------------------------------
    # RELASI
    # ----------------------------------------------------------
    # Relasi ke tabel users
    user: Mapped["User"] = relationship(
        "User",
        back_populates="chats",
    )
    # Satu chat punya banyak pesan
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
    )
    # Satu chat punya satu ringkasan
    summary: Mapped["ChatSummary"] = relationship(
        "ChatSummary",
        back_populates="chat",
        cascade="all, delete-orphan",
        uselist=False,
    )
    # Satu chat punya satu context metadata
    context_metadata: Mapped["ContextMetadata"] = relationship(
        "ContextMetadata",
        back_populates="chat",
        cascade="all, delete-orphan",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<Chat id={self.id_chats} title={self.title}>"