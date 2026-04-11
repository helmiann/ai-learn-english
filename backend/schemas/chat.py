# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chat Schemas
#  File: backend/schemas/chat.py
# ============================================================

from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


# ----------------------------------------------------------
# REQUEST
# ----------------------------------------------------------
class ChatCreate(BaseModel):
    """Schema untuk membuat sesi percakapan baru."""

    title: str = "Percakapan Baru"

    @field_validator("title")
    @classmethod
    def title_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError("Judul tidak boleh kosong")
        if len(v) > 255:
            raise ValueError("Judul maksimal 255 karakter")
        return v


# ----------------------------------------------------------
# RESPONSE
# ----------------------------------------------------------
class ChatResponse(BaseModel):
    """Schema untuk menampilkan satu sesi percakapan."""

    id_chats: int
    id_user: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatListResponse(BaseModel):
    """Schema untuk menampilkan daftar percakapan."""

    chats: List[ChatResponse]
    total: int = 0

    def model_post_init(self, __context) -> None:
        self.total = len(self.chats)