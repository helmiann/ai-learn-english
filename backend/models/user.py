# ============================================================
#  ENGLISH GRAMMAR CHATBOT — User Model
#  File: backend/models/user.py
#  Tabel: users
# ============================================================

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class User(Base):
    __tablename__ = "users"

    # ----------------------------------------------------------
    # KOLOM
    # ----------------------------------------------------------
    id_user: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ----------------------------------------------------------
    # RELASI
    # ----------------------------------------------------------
    # Satu user bisa punya banyak chat
    chats: Mapped[list["Chat"]] = relationship(
        "Chat",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id_user} username={self.username}>"