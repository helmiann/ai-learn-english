# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Message Schemas
#  File: backend/schemas/message.py
# ============================================================

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


# ----------------------------------------------------------
# REQUEST
# ----------------------------------------------------------
class MessageRequest(BaseModel):
    """Schema untuk mengirim pesan ke chatbot."""

    content: str

    @field_validator("content")
    @classmethod
    def content_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError("Pesan tidak boleh kosong")
        if len(v) > 2000:
            raise ValueError("Pesan maksimal 2000 karakter")
        return v


# ----------------------------------------------------------
# RESPONSE
# ----------------------------------------------------------
class MessageResponse(BaseModel):
    """Schema untuk menampilkan satu pesan."""

    id_chatmassages: int
    id_chats: int
    role: str                       # "user" atau "assistant"
    contents: str
    timestamp: datetime
    token_used: Optional[int] = 0

    model_config = {"from_attributes": True}


class MessageListResponse(BaseModel):
    """Schema untuk menampilkan daftar pesan dalam satu chat."""

    messages: List[MessageResponse]
    total: int = 0

    def model_post_init(self, __context) -> None:
        self.total = len(self.messages)


# ----------------------------------------------------------
# GRAMMAR CHECK RESPONSE
# Dipakai jika frontend minta cek grammar sebelum kirim pesan
# ----------------------------------------------------------
class GrammarCheckRequest(BaseModel):
    """Schema untuk request pengecekan grammar."""

    text: str

    @field_validator("text")
    @classmethod
    def text_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError("Teks tidak boleh kosong")
        return v


class GrammarErrorSchema(BaseModel):
    """Schema untuk satu kesalahan grammar."""

    message: str
    short_message: str
    bad_text: str
    replacements: List[str]
    offset: int
    length: int
    category: str


class GrammarCheckResponse(BaseModel):
    """Schema untuk hasil pengecekan grammar."""

    original_text: str
    corrected_text: str
    is_correct: bool
    error_count: int
    errors: List[GrammarErrorSchema]
    feedback: str                   # Teks feedback ramah untuk siswa