# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Context Metadata Model
#  File: backend/models/context_metadata.py
#  Tabel: context_metadata
# ============================================================

from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ContextMetadata(Base):
    __tablename__ = "context_metadata"

    # ----------------------------------------------------------
    # KOLOM
    # ----------------------------------------------------------
    id_contextmetadata: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    id_chats: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id_chats", ondelete="CASCADE"),
        nullable=False,
        unique=True,    # Satu chat hanya boleh punya satu context metadata
        index=True,
    )
    context_data: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        # Menyimpan konteks dalam format JSON string
        # Contoh: '{"topics": ["present tense", "verb to be"], "level": "beginner"}'
    )

    # ----------------------------------------------------------
    # RELASI
    # ----------------------------------------------------------
    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="context_metadata",
    )

    def __repr__(self) -> str:
        return (
            f"<ContextMetadata id={self.id_contextmetadata} "
            f"chat={self.id_chats}>"
        )