# ============================================================
#  ENGLISH GRAMMAR CHATBOT — History Routes
#  File: backend/api/routes/history.py
#  Prefix: /api/history
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from core.security import get_current_user_id
from services.chat_service import ChatService
from schemas.message import MessageListResponse
from core.logging import logger


router = APIRouter()


# ----------------------------------------------------------
# GET /api/history/{chat_id}
# Ambil semua pesan dalam satu sesi percakapan
# ----------------------------------------------------------
@router.get(
    "/{chat_id}",
    response_model=MessageListResponse,
    summary="Riwayat pesan dalam percakapan",
)
async def get_chat_history(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Mengembalikan semua pesan dalam satu sesi percakapan.
    Hanya bisa diakses oleh pemilik percakapan.
    """

    service = ChatService(db)

    # Pastikan chat milik user yang login
    chat = await service.get_chat_by_id(chat_id)
    if not chat or chat.id_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Percakapan tidak ditemukan",
        )

    messages = await service.get_messages_by_chat(chat_id)
    logger.info(f"Riwayat diambil: chat={chat_id} user={user_id}")
    return MessageListResponse(messages=messages)


# ----------------------------------------------------------
# GET /api/history/{chat_id}/summary
# Ambil ringkasan percakapan
# ----------------------------------------------------------
@router.get(
    "/{chat_id}/summary",
    summary="Ringkasan percakapan",
)
async def get_chat_summary(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Mengembalikan ringkasan otomatis dari percakapan."""

    service = ChatService(db)

    chat = await service.get_chat_by_id(chat_id)
    if not chat or chat.id_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Percakapan tidak ditemukan",
        )

    summary = await service.get_summary_by_chat(chat_id)
    if not summary:
        return {"chat_id": chat_id, "summary": None}

    return {"chat_id": chat_id, "summary": summary.summary_text}