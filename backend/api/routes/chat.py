# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Chat Routes
#  File: backend/api/routes/chat.py
#  Prefix: /api/chat
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from core.security import get_current_user_id
from services.chat_service import ChatService
from schemas.chat import (
    ChatCreate,
    ChatResponse,
    ChatListResponse,
)
from schemas.message import MessageRequest, MessageResponse
from core.logging import logger


router = APIRouter()


# ----------------------------------------------------------
# POST /api/chat/new
# Memulai sesi percakapan baru
# ----------------------------------------------------------
@router.post(
    "/new",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mulai percakapan baru",
)
async def create_chat(
    chat_data: ChatCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Membuat sesi percakapan baru untuk user yang sedang login."""

    service = ChatService(db)
    chat = await service.create_chat(user_id=user_id, title=chat_data.title)
    logger.info(f"Chat baru dibuat: id={chat.id_chats} user={user_id}")
    return chat


# ----------------------------------------------------------
# POST /api/chat/{chat_id}/message
# Kirim pesan dan dapatkan respons AI
# ----------------------------------------------------------
@router.post(
    "/{chat_id}/message",
    response_model=MessageResponse,
    summary="Kirim pesan ke chatbot",
)
async def send_message(
    chat_id: int,
    message: MessageRequest,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Mengirim pesan ke chatbot dan mendapatkan respons AI.
    Context manager otomatis mengambil riwayat dan membuat ringkasan.
    """

    service = ChatService(db)

    # Pastikan chat milik user yang login
    chat = await service.get_chat_by_id(chat_id)
    if not chat or chat.id_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Percakapan tidak ditemukan",
        )

    response = await service.send_message(
        chat_id=chat_id,
        user_id=user_id,
        content=message.content,
    )

    logger.info(f"Pesan dikirim: chat={chat_id} user={user_id}")
    return response


# ----------------------------------------------------------
# GET /api/chat/list
# Daftar semua percakapan milik user
# ----------------------------------------------------------
@router.get(
    "/list",
    response_model=ChatListResponse,
    summary="Daftar percakapan",
)
async def get_chat_list(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Mengembalikan daftar semua percakapan milik user yang login."""

    service = ChatService(db)
    chats = await service.get_chats_by_user(user_id)
    return ChatListResponse(chats=chats)


# ----------------------------------------------------------
# DELETE /api/chat/{chat_id}
# Hapus percakapan
# ----------------------------------------------------------
@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_200_OK,
    summary="Hapus percakapan",
)
async def delete_chat(
    chat_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Menghapus percakapan beserta semua pesannya."""

    service = ChatService(db)

    chat = await service.get_chat_by_id(chat_id)
    if not chat or chat.id_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Percakapan tidak ditemukan",
        )

    await service.delete_chat(chat_id)
    logger.info(f"Chat dihapus: id={chat_id} user={user_id}")
    return {"message": "Percakapan berhasil dihapus"}