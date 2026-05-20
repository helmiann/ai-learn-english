# ============================================================
#  ENGLISH GRAMMAR CHATBOT — User Service
#  File: backend/services/user_service.py
# ============================================================

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from schemas.user import UserCreate
from core.security import hash_password, verify_password
from core.logging import logger


class UserService:
    """
    Business logic untuk semua urusan user:
    register, login, ambil data user.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    # ----------------------------------------------------------
    # Ambil user berdasarkan ID
    # ----------------------------------------------------------
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id_user == user_id)
        )
        return result.scalar_one_or_none()

    # ----------------------------------------------------------
    # Ambil user berdasarkan username
    # ----------------------------------------------------------
    async def get_by_username(self, username: str) -> Optional[User]:
        username = username.strip().lower()
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    # ----------------------------------------------------------
    # Buat user baru (register)
    # ----------------------------------------------------------
    async def create_user(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username.strip().lower(),
            password_hash=hash_password(user_data.password),
            kelas=user_data.kelas,
            sekolah=user_data.sekolah,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        logger.info(f"User baru dibuat: {user.username}")
        return user

    # ----------------------------------------------------------
    # Autentikasi user (login)
    # ----------------------------------------------------------
    async def authenticate(
        self, username: str, password: str
    ) -> Optional[User]:
        username = username.strip().lower()
        user = await self.get_by_username(username)

        if not user:
            logger.warning(f"Login gagal: username tidak ditemukan ({username})")
            return None

        if not verify_password(password, user.password_hash):
            logger.warning(f"Login gagal: password salah ({username})")
            return None

        return user