# ============================================================
#  ENGLISH GRAMMAR CHATBOT — Auth Routes
#  File: backend/api/routes/auth.py
#  Prefix: /api/auth
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from services.user_service import UserService
from core.security import create_access_token, get_current_user_id
from schemas.user import UserCreate, UserResponse, TokenResponse
from core.logging import logger


router = APIRouter()


# ----------------------------------------------------------
# POST /api/auth/register
# ----------------------------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Daftar akun baru",
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Mendaftarkan akun pengguna baru (Siswa SMP)."""

    service = UserService(db)

    # Cek apakah username sudah dipakai
    existing = await service.get_by_username(user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan",
        )

    user = await service.create_user(user_data)
    logger.info(f"User baru terdaftar: {user.username}")
    return user


# ----------------------------------------------------------
# POST /api/auth/login
# ----------------------------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login dan dapatkan token",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Login menggunakan username & password.
    Mengembalikan JWT access token jika berhasil.
    """

    service = UserService(db)
    user = await service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": str(user.id_user)})
    logger.info(f"Login berhasil: {user.username}")

    return TokenResponse(access_token=token, token_type="bearer")


# ----------------------------------------------------------
# GET /api/auth/me
# ----------------------------------------------------------
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Lihat profil user yang sedang login",
)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Mengembalikan data profil user yang sedang login."""

    service = UserService(db)
    user = await service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan",
        )

    return user